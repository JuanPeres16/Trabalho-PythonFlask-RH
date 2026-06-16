document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const message = form.getAttribute("data-confirm") || "Confirmar acao?";
            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll("form[data-validate]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const invalid = [...form.querySelectorAll("[required]")].find((field) => {
                return !String(field.value || "").trim();
            });

            if (invalid) {
                event.preventDefault();
                invalid.focus();
                invalid.reportValidity();
            }
        });
    });
});
