Name:           plexus-build-api
Version:        0.0.7
Release:        3
Summary:        Plexus Build API

Group:          Development/Java
License:        ASL 2.0
URL:            https://github.com/sonatype/sisu-build-api
#Fetched from https://github.com/sonatype/sisu-build-api/tarball/plexus-build-api-0.0.7
Source0:        sonatype-sisu-build-api-plexus-build-api-0.0.7-0-g883ea67.tar.gz

Patch0:         %{name}-migration-to-component-metadata.patch

BuildArch: noarch

BuildRequires: java-devel >= 1.6.0
BuildRequires: maven
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
BuildRequires: plexus-container-default
BuildRequires: plexus-utils
BuildRequires: forge-parent
BuildRequires: spice-parent
BuildRequires: junit
BuildRequires: plexus-containers-component-metadata
BuildRequires: maven-shared-reporting-impl
BuildRequires: plexus-digest
BuildRequires: maven-surefire-provider-junit4

Requires: plexus-container-default
Requires: plexus-utils
Requires: jpackage-utils
Requires: spice-parent
Requires: java

%description
Plexus Build API

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n sonatype-sisu-build-api-f1f8849

%patch0 -p1

%build
mvn-rpmbuild install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/plexus
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/plexus/%{name}.jar

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.plexus-%{name}.pom

%add_maven_depmap JPP.plexus-%{name}.pom plexus/%{name}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/plexus/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/plexus/%{name}/

%files
%{_javadir}/plexus/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/plexus/%{name}

