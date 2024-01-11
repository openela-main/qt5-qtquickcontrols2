%global qt_module qtquickcontrols2

%global build_tests 1

Name:    qt5-%{qt_module}
Summary: Qt5 - module with set of QtQuick controls for embedded
Version: 5.15.3
Release: 1%{?dist}
License: GPLv2+ or LGPLv3 and GFDL
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-opensource-src-%{version}.tar.xz

# filter qml provides
%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtbase-private-devel
#libQt53DRender.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Core.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Gui.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Qml.so.5(Qt_5_PRIVATE_API)(64bit)
#libQt5Quick.so.5(Qt_5_PRIVATE_API)(64bit)
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel

Requires: qt5-qtdeclarative%{?_isa} >= %{version}
Requires: qt5-qtgraphicaleffects%{_isa} >= %{version}

%description
The Qt Labs Controls module provides a set of controls that can be used to
build complete interfaces in Qt Quick.

Unlike Qt Quick Controls, these controls are optimized for embedded systems
and so are preferred for hardware with limited resources.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:        Examples for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%if 0%{?build_tests}
%package tests
Summary: Unit tests for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
%{summary}.
%endif


%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}


%build
%{qmake_qt5}

%make_build

%if 0%{?build_tests}
make sub-tests %{?_smp_mflags} -k ||:
%endif


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?build_tests}
# Install tests for gating
mkdir -p %{buildroot}%{_qt5_libdir}/qt5
find ./tests -not -path '*/\.*' -type d | while read LINE
do
    mkdir -p "%{buildroot}%{_qt5_libdir}/qt5/$LINE"
done
find ./tests -not -path '*/\.*' -not -name '*.h' -not -name '*.cpp' -not -name '*.pro' -not -name 'uic_wrapper.sh' -not -name 'Makefile' -not -name 'target_wrapper.sh' -type f | while read LINE
do
    cp -r --parents "$LINE" %{buildroot}%{_qt5_libdir}/qt5/
done
%endif


## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# Remove .la leftovers
rm -f %{buildroot}%{_qt5_libdir}/libQt5*.la


%ldconfig_scriptlets

%files
%license LICENSE.LGPLv3 LICENSE.GPLv3
%{_qt5_libdir}/libQt5QuickTemplates2.so.5*
%{_qt5_libdir}/libQt5QuickControls2.so.5*
%{_qt5_qmldir}/Qt/labs/calendar
%{_qt5_qmldir}/Qt/labs/platform
%{_qt5_archdatadir}/qml/QtQuick/Controls.2/
%{_qt5_archdatadir}/qml/QtQuick/Templates.2/

%files examples
%{_qt5_examplesdir}/quickcontrols2/

%files devel
%{_qt5_headerdir}/
%{_qt5_libdir}/pkgconfig/*.pc
%{_qt5_libdir}/libQt5QuickTemplates2.so
%{_qt5_libdir}/libQt5QuickControls2.so
%{_qt5_libdir}/libQt5QuickTemplates2.prl
%{_qt5_libdir}/libQt5QuickControls2.prl
%{_qt5_libdir}/qt5/mkspecs/modules/*
%{_libdir}/cmake/Qt5QuickControls2/
%{_libdir}/cmake/Qt5QuickTemplates2/

%if 0%{?build_tests}
%files tests
%{_qt5_libdir}/qt5/tests
%endif


%changelog
* Mon Mar 28 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.3-1
- 5.15.3
  Resolves: bz#2061399

* Wed Apr 28 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-2
- Rebuild (binutils)
  Resolves: bz#1930050

* Sun Apr 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2
  Resolves: bz#1930050

* Mon Nov 18 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5
  Resolves: bz#1733146

* Mon Dec 10 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.1-2
- Rebuild to fix CET notes
  Resolves: bz#1657248

* Tue Jul 03 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.1-1
- 5.11.1

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.1-1
- 5.10.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Thu Nov 23 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-2
- BR: qt5-qtbase-private-devel

* Mon Oct 09 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-1
- 5.9.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop shadow/out-of-tree builds (#1456211,QTBUG-37417)

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Tue May 09 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Upstream beta 3

* Mon Jan 30 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- New upstream version

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-3
- filter qml provides

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- 5.7.1 dec5 snapshot
- tighten deps

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Tue Jun 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Mon Jun 13 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-0.1
- Prepare 5.7.0

* Sat Jun 11 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 5.6.1-2
- Add qt5-qtgraphicaleffects dependency

* Thu Jun 09 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1

* Sun Apr 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-4
- BR: qt5-qtbase-private-devel qt5-qtdeclarative-private-devel

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org>
- 5.6.0 final release

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.4.rc
- Update to final RC

* Thu Feb 18 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 5.6.0-0.3.rc
- Update to rc

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.2.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 5.6.0-0.1.beta
- Initial packaging
