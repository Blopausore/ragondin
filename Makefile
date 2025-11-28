dev-pipx:
	pipx uninstall ragondin || true
	pipx install --editable .
	pipx runpip ragondin install "BCEmbedding==0.1.5"
