const selectBox = document.getElementById("selectBox");
        const selectedImg = document.getElementById("selectedImg");
        const selectedName = document.getElementById("selectedName");
        const options = document.querySelectorAll(".option");
        // Open / close dropdown
        document.getElementById("selected").addEventListener("click", () => {
            selectBox.classList.toggle("open");
        });
        // Select an option
        options.forEach((opt) => {
            opt.addEventListener("click", () => {
                selectedImg.src = opt.dataset.img;
                selectedImg.alt = opt.dataset.name;
                selectedName.textContent = opt.dataset.name;
                // hide the currently selected option from the list
                options.forEach((o) => o.classList.toggle("hidden", o === opt));
                selectBox.classList.remove("open");
                console.log("Selected:", opt.dataset.name, "->", opt.dataset.img);
            });
        });
        // Close when clicking outside
        document.addEventListener("click", (e) => {
            if (!selectBox.contains(e.target)) selectBox.classList.remove("open");
        });