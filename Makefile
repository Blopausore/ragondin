dev-pipx:
	pipx uninstall ragondin || true
	pipx install --editable .
