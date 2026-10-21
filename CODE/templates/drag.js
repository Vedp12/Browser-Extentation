const workspace = document.getElementById("rightside");
const icons = workspace.querySelectorAll(".redbox");

const DRAG_THRESHOLD = 5; // pixels before we consider it a drag

icons.forEach((icon) => {
    let startPointerX = 0, startPointerY = 0;
    let startOffsetX = 0, startOffsetY = 0;
    let offsetX = 0, offsetY = 0;
    let dragging = false;
    let pointerDown = false;

    icon.addEventListener("pointerdown", (e) => {
        if (e.pointerType === "mouse" && e.button !== 0) return;

        pointerDown = true;

        startPointerX = e.clientX;
        startPointerY = e.clientY;

        startOffsetX = offsetX;
        startOffsetY = offsetY;

        // NOTE: no preventDefault() here — that's what was killing the link click.
    });

    icon.addEventListener("pointermove", (e) => {
        if (!pointerDown) return;

        const dx = e.clientX - startPointerX;
        const dy = e.clientY - startPointerY;

        // Only start dragging after the pointer moves past the threshold.
        // Small movements let the click reach the <a> tag.
        if (!dragging) {
            if (Math.abs(dx) < DRAG_THRESHOLD && Math.abs(dy) < DRAG_THRESHOLD) {
                return;
            }
            dragging = true;
            icon.classList.add("dragging");
            e.preventDefault();
            icon.setPointerCapture(e.pointerId); // capture only once dragging
        }

        const workspaceRect = workspace.getBoundingClientRect();
        const iconRect = icon.getBoundingClientRect();

        let mdx = e.clientX - startPointerX;
        let mdy = e.clientY - startPointerY;

        const minX = workspaceRect.left + workspace.clientLeft - iconRect.left + offsetX;
        const minY = workspaceRect.top + workspace.clientTop - iconRect.top + offsetY;
        const maxX = workspaceRect.right - workspace.clientLeft - iconRect.right + offsetX;
        const maxY = workspaceRect.bottom - workspace.clientTop - iconRect.bottom + offsetY;

        mdx = Math.max(minX, Math.min(mdx, maxX));
        mdy = Math.max(minY, Math.min(mdy, maxY));

        offsetX = startOffsetX + mdx;
        offsetY = startOffsetY + mdy;

        icon.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
    });

    function stopDragging() {
        pointerDown = false;
        dragging = false;
        icon.classList.remove("dragging");
    }

    icon.addEventListener("pointerup", stopDragging);
    icon.addEventListener("pointercancel", stopDragging);
    icon.addEventListener("lostpointercapture", stopDragging);
});