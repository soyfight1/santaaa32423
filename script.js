document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const themeToggle = document.getElementById('themeToggle');
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.section');
    const htmlElement = document.documentElement;

    // Inicializar primera sección como activa
    if (sections.length > 0) {
        sections[0].classList.add('active');
        if (navButtons.length > 0) {
            navButtons[0].classList.add('active');
        }
    }

    // Función para cambiar de sección
    function showSection(sectionId) {
        // Ocultar todas las secciones
        sections.forEach(section => {
            section.classList.remove('active');
        });

        // Quitar clase active de todos los botones
        navButtons.forEach(btn => {
            btn.classList.remove('active');
        });

        // Mostrar sección seleccionada
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Activar botón correspondiente
        navButtons.forEach(btn => {
            if (btn.getAttribute('data-section') === sectionId) {
                btn.classList.add('active');
            }
        });

        // Scroll suave al top
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    // Event listeners para botones de navegación
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);
        });
    });

    // Función para cambiar tema
    function toggleTheme() {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Actualizar texto del botón
        if (newTheme === 'dark') {
            themeToggle.textContent = '☀️ Modo Claro';
        } else {
            themeToggle.textContent = '🌙 Modo Oscuro';
        }
    }

    // Cargar tema guardado
    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-theme', savedTheme);
    if (savedTheme === 'dark') {
        themeToggle.textContent = '☀️ Modo Claro';
    }

    // Event listener para toggle de tema
    themeToggle.addEventListener('click', toggleTheme);

    // Navegación con teclado
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
            const activeButton = document.querySelector('.nav-btn.active');
            const allButtons = Array.from(navButtons);
            const currentIndex = allButtons.indexOf(activeButton);
            
            let newIndex;
            if (e.key === 'ArrowLeft') {
                newIndex = currentIndex > 0 ? currentIndex - 1 : allButtons.length - 1;
            } else {
                newIndex = currentIndex < allButtons.length - 1 ? currentIndex + 1 : 0;
            }
            
            const newSection = allButtons[newIndex].getAttribute('data-section');
            showSection(newSection);
        }
    });

    // Búsqueda de texto (Ctrl+F mejorado)
    let searchBox = null;
    
    function createSearchBox() {
        if (searchBox) return;
        
        searchBox = document.createElement('div');
        searchBox.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border: 2px solid #3498db;
            border-radius: 5px;
            padding: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        `;
        
        searchBox.innerHTML = `
            <input type="text" id="searchInput" placeholder="Buscar en el texto..." style="
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
                width: 200px;
            ">
            <button onclick="this.parentElement.remove(); searchBox = null;" style="
                margin-left: 5px;
                padding: 5px 10px;
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 3px;
                cursor: pointer;
            ">✕</button>
        `;
        
        document.body.appendChild(searchBox);
        
        const searchInput = document.getElementById('searchInput');
        searchInput.focus();
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const allText = document.querySelectorAll('.text, .stage-direction');
            
            allText.forEach(element => {
                const text = element.textContent.toLowerCase();
                if (searchTerm && text.includes(searchTerm)) {
                    element.style.backgroundColor = 'yellow';
                } else {
                    element.style.backgroundColor = '';
                }
            });
        });
    }

    // Atajo de teclado para búsqueda
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'f') {
            e.preventDefault();
            createSearchBox();
        }
    });

    // Función para imprimir
    function printTranscript() {
        // Mostrar todas las secciones para impresión
        sections.forEach(section => {
            section.style.display = 'block';
        });
        
        window.print();
        
        // Restaurar vista normal después de imprimir
        setTimeout(() => {
            sections.forEach(section => {
                section.style.display = '';
            });
            const activeSection = document.querySelector('.section.active');
            if (activeSection) {
                activeSection.style.display = 'block';
            }
        }, 100);
    }

    // Agregar botón de impresión
    const printButton = document.createElement('button');
    printButton.textContent = '🖨️ Imprimir';
    printButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 100;
        transition: all 0.3s ease;
    `;
    
    printButton.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
    });
    
    printButton.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
    
    printButton.addEventListener('click', printTranscript);
    document.body.appendChild(printButton);

    // Indicador de progreso de lectura
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 4px;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        width: 0%;
        z-index: 1000;
        transition: width 0.3s ease;
    `;
    document.body.appendChild(progressBar);

    // Actualizar barra de progreso al hacer scroll
    window.addEventListener('scroll', function() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });

    // Función para copiar texto seleccionado
    document.addEventListener('mouseup', function() {
        const selection = window.getSelection().toString();
        if (selection.length > 10) {
            // Crear tooltip temporal
            const tooltip = document.createElement('div');
            tooltip.textContent = 'Texto seleccionado - Presiona Ctrl+C para copiar';
            tooltip.style.cssText = `
                position: fixed;
                bottom: 60px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                z-index: 1000;
                animation: fadeInOut 3s ease;
            `;
            
            document.body.appendChild(tooltip);
            setTimeout(() => tooltip.remove(), 3000);
        }
    });

    // Agregar animación CSS para tooltip
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInOut {
            0% { opacity: 0; transform: translateX(-50%) translateY(10px); }
            20% { opacity: 1; transform: translateX(-50%) translateY(0); }
            80% { opacity: 1; transform: translateX(-50%) translateY(0); }
            100% { opacity: 0; transform: translateX(-50%) translateY(10px); }
        }
    `;
    document.head.appendChild(style);
});