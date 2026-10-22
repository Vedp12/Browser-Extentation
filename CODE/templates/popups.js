    const openbutton = document.getElementById("open-maintoolbar-btn");
        const closebutton = document.getElementById("close-maintoolbar-btn");
        const modalContainer = document.getElementById("modalContainer");

        openbutton.addEventListener("click", () => {
            modalContainer.classList.add("show");
        });

        closebutton.addEventListener("click", () => {
            modalContainer.classList.remove("show");
        });

        modalContainer.addEventListener("click", (e) => {
            if (e.target === modalContainer) {
                modalContainer.classList.remove("show");
            }
        });

        // * Passowrd container
        const openbutton_password = document.getElementById("open-modal-password-btn");
        const closebutton_password = document.getElementById("close-modal-password-btn");
        const modalContainer_password = document.getElementById("modal-password-container");

        openbutton_password.addEventListener("click", () => {
            modalContainer_password.classList.add("show");
        });

        closebutton_password.addEventListener("click", () => {
            modalContainer_password.classList.remove("show");
        });

        modalContainer_password.addEventListener("click", (e) => {
            if (e.target === modalContainer_password) {
                modalContainer_password.classList.remove("show");
            }
        });


        const openbutton_additem = document.getElementById("open-modal-additem-btn");
        const modalContainer_additem = document.getElementById("modal-additem-container");
        const closebutton_additem = document.getElementById("Additem-id-btn");

        closebutton_additem.addEventListener("click", () => {
            modalContainer_additem.classList.remove("show");
        });

        openbutton_additem.addEventListener("click", () => {
            modalContainer_additem.classList.add("show");
        });

        modalContainer_additem.addEventListener("click", (e) => {
            if (e.target === modalContainer_additem) {
                modalContainer_additem.classList.remove("show");
            }
        });
