// Função para carregar o JSON e criar as imagens
async function loadAsciiImages() {
	try {
		const response = await fetch("data.json");
		const data = await response.json();
		const gallery = document.getElementById("ascii-gallery");

		data.forEach((imageSet) => {
			// Cria um elemento de imagem
			const asciiImage = document.createElement("img");
			asciiImage.classList.add("ascii-image");

			// Salva o conjunto de imagens no atributo 'data-images'
			asciiImage.setAttribute("data-images", JSON.stringify(imageSet)); // Salva o array de URLs

			// Define a primeira imagem como inicial (lazy loading será aplicado)
			asciiImage.setAttribute("data-srcset", imageSet[imageSet.length-1]);
			gallery.appendChild(asciiImage);
		});

		// Ativa o lazy loading das imagens
		enableLazyLoad();

		// Adiciona o comportamento de slideshow
		enableSlideshow();
	} catch (error) {
		console.error("Erro ao carregar as imagens ASCII:", error);
	}
}

// Função de lazy loading usando IntersectionObserver
function enableLazyLoad() {
	const images = document.querySelectorAll("img[data-srcset]");

	const observer = new IntersectionObserver((entries, observer) => {
		entries.forEach((entry) => {
			if (entry.isIntersecting) {
				const img = entry.target;

				// Move o conteúdo de 'data-srcset' para 'src' e 'srcset'
				img.src = img.dataset.srcset;
				img.srcset = img.dataset.srcset;

				// Remove o atributo 'data-srcset' e para de observar a imagem
				img.removeAttribute("data-srcset");
				observer.unobserve(img);
			}
		});
	});

	// Observa cada imagem que tem o atributo 'data-srcset'
	images.forEach((img) => observer.observe(img));
}

// Função para habilitar o slideshow ao passar o mouse
function enableSlideshow() {
	const images = document.querySelectorAll("img[data-images]");

	images.forEach((img) => {
		let interval;
		const imageSet = JSON.parse(img.getAttribute("data-images")); // Pega o array de imagens
		let currentIndex = 0;

		// Função para iniciar o slideshow
		function startSlideshow() {
			interval = setInterval(() => {
				currentIndex = (currentIndex + 1) % imageSet.length; // Alterna entre os índices
				img.src = imageSet[currentIndex]; // Altera a imagem atual
			}, 1000); // Troca a imagem a cada 1 segundo
		}

		// Função para parar o slideshow
		function stopSlideshow() {
			clearInterval(interval); // Interrompe o intervalo
			img.src = imageSet[0]; // Volta para a primeira imagem
		}

		// Eventos de mouse para iniciar/parar o slideshow
		img.addEventListener("mouseenter", startSlideshow);
		img.addEventListener("mouseleave", stopSlideshow);
	});
}

// Chama a função ao carregar a página
window.onload = loadAsciiImages;
