// Carrega o arquivo JSON e exibe os dados
async function loadAsciiImages() {
	try {
		const response = await fetch("data.json");
		const data = await response.json();
		const gallery = document.getElementById("ascii-gallery");


		data.forEach((image) => {
			const asciiImage = document.createElement("img");
			asciiImage.classList.add("ascii-image");
			asciiImage.src = image; // Exibe o conteúdo ASCII
			gallery.appendChild(asciiImage);
		});
	} catch (error) {
		console.error("Erro ao carregar as imagens ASCII:", error);
	}
}

// Chama a função ao carregar a página
window.onload = loadAsciiImages;
