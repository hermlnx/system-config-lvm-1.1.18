# Build instructions

## Ubuntu PPA deployment steps
- debuild -S -d -us -uc
- pbuilder-dist focal build ../[filename].dsc
- debuild -S -sd
- dput [ppa name] [filename]_source.changes
  
Ref:  https://packaging.ubuntu.com/html/packaging-new-software.html 

## Notes on building system-config-lvm in RHEL/CentOS/Fedora
You will need automake-1.7 and aclocal-1.7
1. type './autogen.sh'
2. type 'make'
3. type 'make srpm'