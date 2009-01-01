%define		_class		PEAR
%define		_subclass	Frontend
%define		_status		beta
%define		_pearname	%{_class}_%{_subclass}_Gtk

Summary:	%{_pearname} - GTK+ (Desktop) PEAR Package Manager
Name:		php-pear-%{_pearname}
Version:	0.4.0
Release:	%mkrel 10
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/PEAR_Frontend_Gtk/
#Requires:	php4-gtk
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Desktop Interface to the PEAR Package Manager.

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Gtk/xpm

install %{_pearname}-%{version}/Gtk.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}
install %{_pearname}-%{version}/Gtk/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Gtk
install %{_pearname}-%{version}/Gtk/*.glade %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Gtk
install %{_pearname}-%{version}/Gtk/xpm/*.xpm %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Gtk/xpm

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%dir %{_datadir}/pear/%{_class}/%{_subclass}/Gtk
%dir %{_datadir}/pear/%{_class}/%{_subclass}/Gtk/xpm
%{_datadir}/pear/%{_class}/%{_subclass}/*.php
%{_datadir}/pear/%{_class}/%{_subclass}/Gtk/*.php
%{_datadir}/pear/%{_class}/%{_subclass}/Gtk/*.glade
%{_datadir}/pear/%{_class}/%{_subclass}/Gtk/xpm/*
%{_datadir}/pear/packages/%{_pearname}.xml


