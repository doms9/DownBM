setup:
	@if [ -f ./DownBM.exe ] || [ -f ./DownBM ]; then \
		printf "Executable exists..."; \
	else \
		[ -d ./Build/ ] || mkdir Build; \
		[ -x "$(command -v pyinstaller)" ] && printf "Building...\n" || python3 -m pip install pyinstaller; \
		python3 -m pip install requests pyqt5 remotezip; \
		pyinstaller -Fyw ./source.pyw --distpath="./" --workpath="./Build/" --specpath="./Build/" -i="../icon.ico" -n="DownBM"; \
		rm -rf ./Build/; \
		clear; \
		printf "Successfully built DownBM!"; \
	fi;
