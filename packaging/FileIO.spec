Name:          FileIO
Version:       %{version}
Release:       1%{?dist}
Summary:       An implemnetation of File IO for C++
Group:         Development/Tools
License:       MIT
BuildRequires: probecmake >= 2.8
ExclusiveArch: x86_64

%description

%prep
cd ~/rpmbuild/BUILD
rm -rf %{name}
mkdir -p %{name}
cd %{name}
tar xzf ~/rpmbuild/SOURCES/%{name}-%{version}.tar.gz
if [ $? -ne 0 ]; then
   exit $?
fi

%build
# SKIP_BUILD_RPATH, CMAKE_SKIP_BUILD_RPATH, 
cd %{name}/
PATH=/usr/local/probe/bin:$PATH
rm -f  CMakeCache.txt
cd 3rdparty
unzip -u gtest-1.7.0.zip
cd ..


if [ "%{buildtype}" == "-DUSE_DEBUG_COVERAGE=OFF" ]; then
   echo "buildtype: -DUSE_DEBUG_COVERAGE=OFF --> PRODUCTION"
   /usr/local/probe/bin/cmake -DVERSION=%{version} -DCMAKE_CXX_COMPILER_ARG1:STRING=' -fPIC -Ofast -m64 -Wl,-rpath -Wl,. -Wl,-rpath -Wl,/usr/local/probe/lib -Wl,-rpath -Wl,/usr/local/probe/lib64 ' -DCMAKE_BUILD_TYPE:STRING=Release -DBUILD_SHARED_LIBS:BOOL=ON -DCMAKE_CXX_COMPILER=/usr/local/probe/bin/g++
elif [ "%{buildtype}" == "-DUSE_DEBUG_COVERAGE=ON" ]; then
   echo "buildtype: -DUSE_DEBUG_COVERAGE=ON";
   /usr/local/probe/bin/cmake -DUSE_LR_DEBUG=ON -DVERSION=%{version} -DCMAKE_CXX_COMPILER_ARG1:STRING=' -Wall -Werror -g -gdwarf-2 -fprofile-arcs -ftest-coverage -O0 -fPIC -m64 -Wl,-rpath -Wl,. -Wl,-rpath -Wl,/usr/local/probe/lib -Wl,-rpath -Wl,/usr/local/probe/lib64 ' -DCMAKE_CXX_COMPILER=/usr/local/probe/bin/g++
else
   echo "unknown buildtype %{buildtype}"
   exit 1
fi

make VERSION=1 -j6
sudo ./UnitTestRunner


mkdir -p $RPM_BUILD_ROOT/usr/local/probe/lib
cp -rfd lib%{name}.so* $RPM_BUILD_ROOT/usr/local/probe/lib
mkdir -p $RPM_BUILD_ROOT/usr/local/probe/include
cp src/*.h $RPM_BUILD_ROOT/usr/local/probe/include


%post

%preun

%postun

%files
%defattr(-,dpi,dpi,-)
/usr/local/probe/lib
/usr/local/probe/include
