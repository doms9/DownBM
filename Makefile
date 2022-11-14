
setup:
	@if [ -f ./DownBM.exe ] || [ -f ./DownBM ]; then \
		printf "Executable exists..."; \
	else \
		[ -d ./Build/ ] || mkdir Build; \
		[ -x "$(command -v pyinstaller)" ] && printf "Building...\n" || python3 -m pip install pyinstaller; \
		python3 -m pip install requests pyqt5 remotezip; \
		pyinstaller -Fyc ./source.pyw --distpath="./" --workpath="./Build/" --specpath="./Build/" -i="../icon.ico" -n="DownBM"; \
		rm -rf ./Build/; \
		printf "\nSuccessfully built DownBM!"; \
	fi;
rf:
	@if [ -f qt2py.exe ] || [ -f qt2py ]; then \
        printf "qt2py exists\n\nMake sure to add it to your PATH!"; \
    else \
		printf "Building...\n"; \
        [ -d Build ] || mkdir Build; \
		${PYTHON} -m pip install pyinstaller pyqt5 pyqt6; \
		${PYINST} -y -F --console ./source.py --distpath="." --workpath="Build" --specpath="Build" -n="qt2py"; \
		sudo cp qt2py* /usr/local/bin/; \
		rm -rf Build/; \
		printf "\nSuccessfully built qt2py!"; \
    fi

clean:
	@printf "Cleaning...\n"
	@if [ -d Build ]; then \
		rm -rf Build/; \
	fi