// Função para carregar o JSON e criar as imagens
async function loadAsciiImages(fontSize = 50) {
	try {
		const response = await fetch("data.json");
		const data = await response.json();
		const gallery = document.getElementById("ascii-gallery");

		let scale = 1;
		switch(fontSize) {
			case "14": break;
			case "25": scale = .90; break;
			case "40": scale = .80; break;
			case "50": scale = .75; break;
			case "100": scale = .50; break;
			case "110": scale = .30; break;
		}

		// Verifica se o tamanho selecionado existe nos dados
		if (data[fontSize]) {
			// Limpa o conteúdo da galeria antes de adicionar as novas imagens
			gallery.innerHTML = "";

			// Adiciona as imagens do conjunto selecionado
			data[fontSize].forEach((imageSet) => {
				const div = document.createElement("div")
				const asciiImage = document.createElement("img");
				asciiImage.classList.add("ascii-image");
				asciiImage.setAttribute("data-srcset", imageSet);
				//asciiImage.style.transform = `scale(${scale})`
				div.appendChild(asciiImage)
				gallery.appendChild(div);
			});

			// Ativa o lazy loading das imagens
			enableLazyLoad();
		} else {
			console.warn("Tamanho de fonte não encontrado nos dados.");
		}
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

// Função para abrir/fechar a lista de tamanhos
function toggleFontSizeButtons() {
	const buttons = document.getElementById("font-size-buttons");
	buttons.style.display = buttons.style.display === "none" ? "block" : "none";
}

// Função para selecionar o tamanho da fonte
function selectFontSize(event) {
	const fontSize = event.target.getAttribute("data-font-size");

	// Atualiza a seleção visual dos botões
	document.querySelectorAll(".font-size-button").forEach((button) => {
		button.classList.remove("selected");
	});
	event.target.classList.add("selected");

	// Carrega as imagens com o tamanho selecionado
	loadAsciiImages(fontSize);
}

// Função para adicionar eventos aos botões de tamanho de fonte
function setupFontSizeButtons() {
	const buttons = document.querySelectorAll(".font-size-button");

	buttons.forEach((button) => {
		button.addEventListener("click", selectFontSize);
	});
}

// Chama a função ao carregar a página
window.onload = () => {
	// Carrega as imagens iniciais
	loadAsciiImages(14);

	// Configura os botões de tamanho de fonte
	setupFontSizeButtons();

	// Adiciona o evento de abrir/fechar a lista
	const toggleButton = document.getElementById("font-size-toggle");
	toggleButton.addEventListener("click", toggleFontSizeButtons);
};
