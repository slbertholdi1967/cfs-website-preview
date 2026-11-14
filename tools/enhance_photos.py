"""Professional-style enhancement of the CFS project photos.
Steps: orientation, AI upscale (Real-ESRGAN general x4v3) when small, vertical/keystone correction,
white balance, levels, local contrast, vibrance, gentle denoise, output sharpening."""
import sys, json, math, os, numpy as np, cv2
from PIL import Image, ImageOps

# Real-ESRGAN general x4v3 ONNX model, used only for small photos. Optional: without it small photos are kept at
# their size (phone photos are large enough). Set ENHANCE_MODEL to the .onnx file to enable it.
M = os.environ.get('ENHANCE_MODEL', '')
try:  # iPhone HEIC photos uploaded from CFS Core
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass
SESS = None


def sess():
    global SESS
    if SESS is None:
        import onnxruntime as ort  # only needed for the optional upscale model
        so = ort.SessionOptions(); so.intra_op_num_threads = 4
        SESS = ort.InferenceSession(M, so, providers=['CPUExecutionProvider'])
    return SESS


def load(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)


def upscale4(img, T=320, P=16):
    s = sess(); name = s.get_inputs()[0].name
    h, w = img.shape[:2]
    x = img[:, :, ::-1].astype(np.float32) / 255.0
    pad = cv2.copyMakeBorder(x, P, P + T, P, P + T, cv2.BORDER_REFLECT)
    out = np.zeros((h * 4, w * 4, 3), np.float32)
    step = T - 2 * P
    for yy in range(0, h, step):
        for xx in range(0, w, step):
            t = np.ascontiguousarray(pad[yy:yy + T, xx:xx + T].transpose(2, 0, 1))[None]
            r = s.run(None, {name: t})[0][0][:, 4 * P:4 * (T - P), 4 * P:4 * (T - P)].transpose(1, 2, 0)
            hh = min(4 * step, 4 * h - 4 * yy); ww = min(4 * step, 4 * w - 4 * xx)
            out[4 * yy:4 * yy + hh, 4 * xx:4 * xx + ww] = r[:hh, :ww]
    return (np.clip(out, 0, 1) * 255).round().astype(np.uint8)[:, :, ::-1]


def resize_long(img, L):
    h, w = img.shape[:2]
    k = L / max(h, w)
    if abs(k - 1) < 1e-3:
        return img
    return cv2.resize(img, (round(w * k), round(h * k)), interpolation=cv2.INTER_AREA if k < 1 else cv2.INTER_LANCZOS4)


def verticals(img):
    """Near-vertical line segments: list of (x_at_top, x_at_bottom, length) in a 1200px working copy."""
    small = resize_long(img, 1200)
    g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (3, 3), 0)
    e = cv2.Canny(g, 60, 160)
    h, w = g.shape
    lines = cv2.HoughLinesP(e, 1, np.pi / 720, threshold=80, minLineLength=h // 7, maxLineGap=6)
    segs = []
    if lines is None:
        return small.shape, segs
    for x1, y1, x2, y2 in lines.reshape(-1, 4).tolist():
        if y2 == y1:
            continue
        ang = math.degrees(math.atan2(x2 - x1, y2 - y1))
        if ang > 90: ang -= 180
        if ang < -90: ang += 180
        if abs(ang) > 12:
            continue
        # x at top (y=0) and at bottom (y=h)
        k = (x2 - x1) / (y2 - y1)
        xt = x1 - k * y1; xb = x1 + k * (h - y1)
        segs.append((xt, xb, math.hypot(x2 - x1, y2 - y1), (x1 + x2) / 2))
    return small.shape, segs


def keystone(img, max_deg=9.0):
    """Make building verticals vertical (2-point perspective correction), conservatively."""
    (h, w, _), segs = verticals(img)
    if len(segs) < 6:
        return img, 'none'
    # Model: each line's lean (xb - xt)/h depends linearly on its horizontal position: lean = a + b * (xmid/w - .5)
    X = np.array([[1, s[3] / w - 0.5] for s in segs]); y = np.array([(s[1] - s[0]) / h for s in segs]); wt = np.array([s[2] for s in segs])
    for _ in range(3):  # robust refit
        A = X * wt[:, None]
        coef, *_ = np.linalg.lstsq(A, y * wt, rcond=None)
        res = np.abs(X @ coef - y)
        keep = res < max(0.02, np.percentile(res, 70))
        X, y, wt = X[keep], y[keep], wt[keep]
        if len(y) < 6:
            return img, 'none'
    a, b = coef
    tilt = math.degrees(math.atan(a)); conv = math.degrees(math.atan(b / 2))
    if abs(tilt) > max_deg or abs(conv) > max_deg:
        return img, f'skip tilt={tilt:.1f} conv={conv:.1f}'
    if abs(tilt) < 0.3 and abs(conv) < 0.3:
        return img, 'ok'
    H, W = img.shape[:2]
    # Where the left/right edges lean: lean at x=0 is a - b/2, at x=W is a + b/2 (fraction of height)
    # Correction: move the top corners so lines become vertical (keep bottom fixed). Use 85% strength (natural look).
    s = 0.85
    lL = (a - b / 2) * s; lR = (a + b / 2) * s
    src = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    # a line leaning lL means top is at x - lL*H relative to bottom: shift the top corner by +lL*H to straighten
    dst = np.float32([[0 + lL * H, 0], [W + lR * H, 0], [W, H], [0, H]])
    Mx = cv2.getPerspectiveTransform(dst, src)
    out = cv2.warpPerspective(img, Mx, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT)
    # crop the empty wedges: find the largest inner rectangle by mapping the source corners
    pts = cv2.perspectiveTransform(np.float32([[[0, 0]], [[W, 0]], [[W, H]], [[0, H]]]), Mx)[:, 0]
    x0 = max(pts[0][0], pts[3][0], 0); x1 = min(pts[1][0], pts[2][0], W)
    y0 = max(pts[0][1], pts[1][1], 0); y1 = min(pts[2][1], pts[3][1], H)
    x0, x1, y0, y1 = int(math.ceil(x0)) + 2, int(x1) - 2, int(math.ceil(y0)) + 2, int(y1) - 2
    if (x1 - x0) < 0.8 * W or (y1 - y0) < 0.8 * H:
        return img, f'skip crop tilt={tilt:.1f} conv={conv:.1f}'
    return out[y0:y1, x0:x1], f'fixed tilt={tilt:.1f} conv={conv:.1f}'


def tone(img):
    src = img
    f = img.astype(np.float32)
    # white balance: partial gray world on mid-tones
    m = f.reshape(-1, 3); lum = m.mean(1)
    mid = m[(lum > 40) & (lum < 220)]
    if len(mid) > 1000:
        avg = mid.mean(0); g = avg.mean()
        gain = 1 + 0.45 * (g / avg - 1)
        f *= np.clip(gain, 0.85, 1.15)
    # levels: 0.4% / 99.6% stretch on luminance
    l = f.mean(2)
    lo, hi = np.percentile(l, 0.4), np.percentile(l, 99.6)
    lo = min(lo, 30); hi = max(hi, 225)
    f = (f - lo) * (255.0 / max(1, hi - lo))
    f = np.clip(f, 0, 255).astype(np.uint8)
    # local contrast on L
    lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)
    L = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8)).apply(L)
    # gentle midtone lift if dark
    meanL = L.mean()
    if meanL < 110:
        gamma = 0.85 if meanL < 90 else 0.92
        L = (255 * (L / 255.0) ** gamma).astype(np.uint8)
    f = cv2.cvtColor(cv2.merge([L, A, B]), cv2.COLOR_LAB2BGR)
    # vibrance: boost low-saturation pixels more
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    sat = hsv[:, :, 1] / 255.0
    boost = 0.16 if sat.mean() < 0.28 else 0.06
    hsv[:, :, 1] = np.clip(255 * (sat + boost * sat * (1 - sat) * 2), 0, 255)
    f = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    # clarity: large-radius unsharp
    blur = cv2.GaussianBlur(f, (0, 0), 18)
    f = cv2.addWeighted(f, 1.12, blur, -0.12, 0)
    # protect whites and light greys: keep the original colour (chroma) where the result is bright
    lo = cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32)
    li = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(np.float32)
    w = np.clip((lo[:, :, 0] - 150) / 70.0, 0, 1)[:, :, None] * 0.85
    lo[:, :, 1:] = lo[:, :, 1:] * (1 - w) + li[:, :, 1:] * w
    # neutralise a leftover cast in the brightest areas (sky, white panels)
    bright = lo[:, :, 0] > 200
    if bright.mean() > 0.03:
        for c in (1, 2):
            d = lo[:, :, c][bright].mean() - 128
            if abs(d) > 2:
                lo[:, :, c] -= d * 0.7 * np.clip((lo[:, :, 0] - 120) / 100.0, 0, 1)
    return cv2.cvtColor(np.clip(lo, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def sharpen(img, amount=0.55, radius=1.0):
    blur = cv2.GaussianBlur(img, (0, 0), radius)
    return cv2.addWeighted(img, 1 + amount, blur, -amount, 0)


def process(src, out_full, out_mid, L_full=2400, L_mid=1200):
    img = load(src)
    h, w = img.shape[:2]
    log = [f'{w}x{h}']
    if max(h, w) < 1900 and M and os.path.exists(M):
        img = upscale4(img)
        log.append('ai-upscale x4')
    elif max(h, w) < 1900:
        log.append('small, no upscale model')
    else:
        img = cv2.fastNlMeansDenoisingColored(resize_long(img, min(max(h, w), 3200)), None, 3, 3, 7, 21)
    img, ks = keystone(img); log.append(ks)
    img = resize_long(img, L_full) if max(img.shape[:2]) > L_full else img
    img = tone(img)
    full = sharpen(img, 0.45, 1.0)
    mid = sharpen(resize_long(img, L_mid), 0.35, 0.8)
    os.makedirs(os.path.dirname(out_full), exist_ok=True); os.makedirs(os.path.dirname(out_mid), exist_ok=True)
    cv2.imwrite(out_full, full, [cv2.IMWRITE_JPEG_QUALITY, 84, cv2.IMWRITE_JPEG_PROGRESSIVE, 1, cv2.IMWRITE_JPEG_OPTIMIZE, 1])
    cv2.imwrite(out_mid, mid, [cv2.IMWRITE_JPEG_QUALITY, 82, cv2.IMWRITE_JPEG_PROGRESSIVE, 1, cv2.IMWRITE_JPEG_OPTIMIZE, 1])
    return ' | '.join(log)


if __name__ == '__main__':
    jobs = json.load(open(sys.argv[1]))
    for src, full, mid in jobs:
        if os.path.exists(full) and os.path.exists(mid):
            continue
        try:
            print(os.path.basename(src), process(src, full, mid), flush=True)
        except Exception as e:
            print('ERROR', src, e, flush=True)
