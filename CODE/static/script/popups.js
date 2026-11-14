// 1. Define configurations for all your modals
const modalConfigs = [
    
    {
        openId: "open-maintoolbar-btn",
        closeId: "close-maintoolbar-btn",
        modalId: "modal-container"
    },
    {
        openId: "open-modal-notes-btn",
        closeId: "notes-modal-close-btn",
        modalId: "modal-container--notes"
    },
    {
        openId: "open-modal-password-btn",
        closeId: "close-modal-password-btn",
        modalId: "modal-password-container"
    },
    {
        openId: "open-modal-additem-btn",
        closeId: "Additem-id-btn",
        modalId: "modal-additem-container"
    },
    {
        openId: "open-modal-qr-btn",
        closeId: "close-qr",
        modalId: "qr-modal-container",
    },
    {
        openId: "open-modal-time-btn",
        closeId: "close-timer-btn",
        modalId: "main-time-container"
    },
    
    {
        openId: "new-notes-btn",
        closeId: "close-note-back-btn",
        modalId: "notes-editor-container"
    },
    {
            openId: "notes-card-edit-btn",
        closeId: "close-note-back-btn",
        modalId: "notes-editor-container"
    }
];

// 2. Initialize and attach event listeners to each modal
modalConfigs.forEach(config => {
    const openBtn = document.getElementById(config.openId);
    const closeBtn = document.getElementById(config.closeId);
    const modal = config.isClass 
        ? document.querySelector(config.modalId) 
        : document.getElementById(config.modalId);

    if (!openBtn || !closeBtn || !modal) {
        console.warn(`Modal elements missing for configuration:`, config);
        return;
    }

    const openModal = () => {
        modal.classList.add("show");
        modal.setAttribute("aria-hidden", "false");
        openBtn.setAttribute("aria-expanded", "true");
    };

    const closeModal = () => {
        modal.classList.remove("show");
        modal.setAttribute("aria-hidden", "true");
        openBtn.setAttribute("aria-expanded", "false");
    };

    // Open/Toggle button click
    openBtn.addEventListener("click", () => {
        if (modal.classList.contains("show")) {
            closeModal();
        } else {
            openModal();
        }
    });

    // Close button click
    closeBtn.addEventListener("click", closeModal);

    // Close when clicking the outer backdrop box
    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });
});

// 3. Global Escape key handler to close any active modal
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        modalConfigs.forEach(config => {
            const modal = config.isClass 
                ? document.querySelector(config.modalId) 
                : document.getElementById(config.modalId);
            
            if (modal && modal.classList.contains("show")) {
                modal.classList.remove("show");
                modal.setAttribute("aria-hidden", "true");
                
                const openBtn = document.getElementById(config.openId);
                if (openBtn) {
                    openBtn.setAttribute("aria-expanded", "false");
                }
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
   
    const newNoteBtn = document.getElementById("new-notes-btn");
    const editorContainer = document.getElementById("notes-editor-container");
    const modalContainer = document.getElementById("modal-container--notes");
    const closeBtn = document.getElementById("notes-modal-close-btn");

    if (newNoteBtn && editorContainer && modalContainer) {
        newNoteBtn.addEventListener("click", () => {
            modalContainer.classList.add("show");
            editorContainer.classList.add("show");
        });
    }

    if (closeBtn && modalContainer && editorContainer) {
        closeBtn.addEventListener("click", () => {
            modalContainer.classList.remove("show");
            editorContainer.classList.remove("show");
        });
    }

    // 2. Handle all Edit Note buttons (using class instead of duplicate IDs)
    const editBtns = document.querySelectorAll(".notes-card-edit-btn");
    editBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (modalContainer && editorContainer) {
                modalContainer.classList.add("show");
                editorContainer.classList.add("show");
            }
        });
    });

    // 3. Close modal when clicking outside the content area
    if (modalContainer) {
        modalContainer.addEventListener("click", (event) => {
            if (event.target === modalContainer) {
                modalContainer.classList.remove("show");
                editorContainer.classList.remove("show");
            }
        });
    }

    // 4. Global Escape key handler
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && modalContainer) {
            modalContainer.classList.remove("show");
            if (editorContainer) {
                editorContainer.classList.remove("show");
            }
        }
    });
});