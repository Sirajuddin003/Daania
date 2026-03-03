/* =====================================================
   GLOWLUXE – FINAL PRODUCTION JAVASCRIPT
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       NAVBAR SCROLL EFFECT
    ===================================================== */
    const navbar = document.querySelector(".navbar");

    if (navbar) {
        window.addEventListener("scroll", () => {
            navbar.classList.toggle("scrolled", window.scrollY > 40);
        });
    }


    /* =====================================================
       MOBILE MENU TOGGLE
    ===================================================== */
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", () => {
            navLinks.classList.toggle("active");
        });

        navLinks.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                navLinks.classList.remove("active");
            });
        });
    }


    /* =====================================================
       SECTION REVEAL (INTERSECTION OBSERVER)
    ===================================================== */
    const sections = document.querySelectorAll("section");

    if ("IntersectionObserver" in window) {
        const sectionObserver = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        sectionObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.15 }
        );

        sections.forEach(section => sectionObserver.observe(section));
    } else {
        // Fallback
        sections.forEach(section => section.classList.add("is-visible"));
    }


    /* =====================================================
       PRODUCT CARD HOVER (DESKTOP + MOBILE SAFE)
    ===================================================== */
    document.querySelectorAll(".product-card").forEach(card => {
        card.addEventListener("mouseenter", () => card.classList.add("hovered"));
        card.addEventListener("mouseleave", () => card.classList.remove("hovered"));

        card.addEventListener("touchstart", () => card.classList.add("hovered"));
        card.addEventListener("touchend", () => card.classList.remove("hovered"));
    });


    /* =====================================================
       BUTTON PRESS MICRO-INTERACTION
    ===================================================== */
    document.querySelectorAll(".btn").forEach(btn => {
        btn.addEventListener("click", () => {
            btn.style.transform = "scale(0.96)";
            setTimeout(() => btn.style.transform = "", 150);
        });
    });


    /* =====================================================
       ADD TO CART (AJAX – DJANGO FRIENDLY)
    ===================================================== */
    const cartCount = document.querySelector(".cart-count");

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", e => {
            e.preventDefault();

            const url = button.getAttribute("href");
            if (!url) return;

            fetch(url, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && cartCount) {
                    cartCount.textContent = data.cart_count;

                    cartCount.classList.add("pulse");
                    setTimeout(() => {
                        cartCount.classList.remove("pulse");
                    }, 350);
                }
            })
            .catch(err => console.error("Add to Cart Error:", err));
        });
    });
    

    /* =====================================================
       HERO PARALLAX (DESKTOP ONLY)
    ===================================================== */
    const heroBlob = document.querySelector(".hero-blob");

    if (heroBlob && window.innerWidth > 768) {
        window.addEventListener("mousemove", e => {
            const x = (window.innerWidth / 2 - e.clientX) / 45;
            const y = (window.innerHeight / 2 - e.clientY) / 45;
            heroBlob.style.transform = `translate(${x}px, ${y}px)`;
        });
    }


    /* =====================================================
       EMPTY CART ICON MICRO ANIMATION
    ===================================================== */
    const emptyCartIcon = document.querySelector(".empty-cart-icon");

    if (emptyCartIcon) {
        let grow = true;

        setInterval(() => {
            emptyCartIcon.style.transform = grow ? "scale(1.08)" : "scale(1)";
            grow = !grow;
        }, 1200);
    }


    /* =====================================================
       GALLERY SMOOTH SCROLL (MOBILE)
    ===================================================== */
    const galleryRow = document.querySelector(".gallery-row");

    if (galleryRow && window.innerWidth < 768) {
        galleryRow.addEventListener("wheel", e => {
            e.preventDefault();
            galleryRow.scrollLeft += e.deltaY;
        }, { passive: false });
    }

});

/* =====================================================
   ADD TO CART BUTTON – PREMIUM INTERACTION
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const cartCount = document.querySelector(".cart-count");
    const addToCartButtons = document.querySelectorAll(".btn.primary.add-to-cart");

    addToCartButtons.forEach(btn => {

        /* PRESS ANIMATION (CONSISTENT WITH ALL BUTTONS) */
        btn.addEventListener("mousedown", () => {
            btn.classList.add("pressed");
        });

        ["mouseup", "mouseleave"].forEach(event => {
            btn.addEventListener(event, () => {
                btn.classList.remove("pressed");
            });
        });

        /* AJAX ADD TO CART */
        btn.addEventListener("click", e => {
            e.preventDefault();

            const url = btn.getAttribute("href");
            if (!url) return;

            /* TEMP BUTTON FEEDBACK */
            const originalText = btn.innerText;
            btn.innerText = "Adding...";
            btn.style.pointerEvents = "none";

            fetch(url, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {

                    /* UPDATE CART COUNT */
                    if (cartCount) {
                        cartCount.textContent = data.cart_count;
                        cartCount.classList.add("pulse");

                        setTimeout(() => {
                            cartCount.classList.remove("pulse");
                        }, 350);
                    }

                    /* SUCCESS FEEDBACK */
                    btn.innerText = "Added ✓";
                    btn.style.transform = "scale(1.04)";

                    setTimeout(() => {
                        btn.innerText = originalText;
                        btn.style.transform = "";
                        btn.style.pointerEvents = "";
                    }, 900);
                }
            })
            .catch(err => {
                console.error("Cart Error:", err);
                btn.innerText = originalText;
                btn.style.pointerEvents = "";
            });
        });
    });

});


