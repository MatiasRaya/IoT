const menu = document.querySelector(".nav-top");
const openMenuBtn = document.querySelector(".open-menu");
const closeMenuBtn = document.querySelector(".close-menu");

function toggleMenu() {
    menu.classList.toggle("menu_opened");
}

openMenuBtn.addEventListener("click", toggleMenu);
closeMenuBtn.addEventListener("click", toggleMenu);

const menuLinks = document.querySelectorAll(".nav-top a[href^=\"#\"]");

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        const id = entry.target.getAttribute("id");
        const menuLink = document.querySelector(`.nav-top a[href^="#${id}"]`)

        if(entry.isIntersecting){
            menuLink.classList.add("selected");
        }
        else{
            menuLink.classList.remove("selected");
        }
    });
}, {rootMargin: "-50% 0px -50% 0px"});

menuLinks.forEach(menuLink => {
    menuLink.addEventListener("click", function() {
        menu.classList.remove("menu_opened");
    })

    const hash = menuLink.getAttribute("href");
    const target = document.querySelector(hash);
    if(target){
        observer.observe(target);
    }
})