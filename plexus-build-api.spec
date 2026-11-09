Name:		plexus-build-api
Version:	1.2.0
Release:	2
Summary:	Incremental build context for Plexus components
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/codehaus-plexus/plexus-build-api
Source0:	https://github.com/codehaus-plexus/plexus-build-api/archive/refs/tags/plexus-build-api-0.0.7.tar.gz
Source1:	LICENSE-2.0.txt
Patch0:	0000-Port-to-plexus-utils-3.3.0.patch
BuildArch:	noarch
BuildRequires:	python
# The maven RPM holds the sisu classes. maven-components owns that coordinate.
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Filesystem build context used by incremental Maven plugins. The
sources are plexus-build-api 0.0.7. The package version stays 1.2.0
because that release already shipped these sources. DefaultBuildContext
is registered as the default BuildContext.

%prep
%autosetup -n plexus-build-api-plexus-build-api-0.0.7 -p1
cp -p %{SOURCE1} .
rm -rf src/test
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.sonatype.plexus")
add(root, "artifactId", "plexus-build-api")
# Upstream tag 0.0.7. The RPM version is 1.2.0 for upgrade ordering.
add(root, "version", "0.0.7")
add(root, "name", "Plexus Build API")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("org.codehaus.plexus", "plexus-utils", "3.6.2"),
    ("org.eclipse.sisu", "org.eclipse.sisu.plexus", "0.9.0.M3"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
mkdir -p src/main/resources/META-INF/plexus
cat > src/main/resources/META-INF/plexus/components.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<component-set>
  <components>
    <component>
      <role>org.sonatype.plexus.build.incremental.BuildContext</role>
      <role-hint>default</role-hint>
      <implementation>org.sonatype.plexus.build.incremental.DefaultBuildContext</implementation>
      <isolated-realm>false</isolated-realm>
    </component>
  </components>
</component-set>
EOF

%files -f .mfiles
%doc LICENSE-2.0.txt
