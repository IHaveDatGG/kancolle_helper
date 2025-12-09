from pathlib import Path
from typing import Optional
import cv2
import numpy as np

# Define the root directory where template images are stored.
_TEMPLATE_ROOT = Path.cwd() / "templates"

# Cache for storing template images and their associated keypoints and descriptors.
_template_cache: dict[str, tuple[np.ndarray, list, np.ndarray]] = {}


def locate(
        image: np.ndarray,
        template_paths: str | list[str],
        ratio_thresh: float = 0.7,
        sim_thresh: float = 0.8
    ) -> Optional[tuple[int, int]]:
    """Locate the template in the given image and return the center point."""
    image, image_kp, image_des = _extract_image_features(image)

    if isinstance(template_paths, str):
        template_paths = [template_paths]

    for template_path in template_paths:
        template, template_kp, template_des = _load_template_features(template_path)

        # Match features and compute homography
        good_matches = _match_features(template_des, image_des, ratio_thresh)
        H = _compute_homography(template_kp, image_kp, good_matches)
        if H is None:
            continue

        # Verification using template matching
        if not _verify_template_match(image, template, H, sim_thresh):
            continue

        # Return center point
        return _compute_template_center(template, H)

    # Return None if no template was matched
    return None


def _load_template_features(path: str) -> tuple[np.ndarray, list, np.ndarray]:
    """Load and cache the template image and extract features."""
    template_path = _resolve_template_path(path)
    if template_path in _template_cache:
        return _template_cache[template_path]

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(template_path)

    kp, des = _detect_features(template)
    _template_cache[template_path] = (template, kp, des)
    return template, kp, des


def _extract_image_features(img: np.ndarray) -> tuple[np.ndarray, list, np.ndarray]:
    """Convert image to grayscale and extract features."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, des = _detect_features(img)
    return gray, kp, des


def _match_features(des_t: np.ndarray, des_i: np.ndarray, threshold=0.7) -> list[cv2.DMatch]:
    """Match template features to image features using FLANN and ratio test."""
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des_t, des_i, k=2)
    return [m for m, n in matches if m.distance < threshold * n.distance]


def _compute_homography(kp1: list, kp2: list, matches: list[cv2.DMatch]) -> Optional[np.ndarray]:
    """Compute homography from matched keypoints. Return None if insufficient matches."""
    if len(matches) < 8:  # need at least 4 points
        return None
    src = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    return H


def _verify_template_match(image: np.ndarray, template: np.ndarray, H: np.ndarray,
        sim_thresh=0.8) -> bool:
    """Warp the template using the homography and verify similarity with template matching."""
    warped = cv2.warpPerspective(template, H, (image.shape[1], image.shape[0]))
    mask = (warped > 0).astype(np.uint8)
    res = cv2.matchTemplate(image, warped, cv2.TM_CCOEFF_NORMED, mask=mask)
    return np.max(res) >= sim_thresh


def _compute_template_center(template: np.ndarray, H: np.ndarray) -> tuple[int, int]:
    """Compute the center of the warped template."""
    h, w = template.shape
    pts = np.float32([[0,0],[w,0],[w,h],[0,h]]).reshape(-1,1,2)
    projected = cv2.perspectiveTransform(pts, H).reshape(4,2)
    center_x = int(np.mean(projected[:,0]))
    center_y = int(np.mean(projected[:,1]))
    return (center_x, center_y)


def _resolve_template_path(path: str) -> str:
    """Return absolute path to template."""
    p = Path(path)
    if p.is_absolute():
        return str(p)
    return str(_TEMPLATE_ROOT / p)


def _detect_features(img: np.ndarray) -> tuple[list, np.ndarray]:
    """Detect SIFT keypoints and descriptors."""
    sift = cv2.SIFT.create()
    kp, des = sift.detectAndCompute(img, None)
    return kp, des
