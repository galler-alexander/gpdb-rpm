Summary:	The programs needed to create and run a Greenplum server
Name:		gpdb	
Version:	5.9.0
Release:	1
License:	Apache License v2.0
Group:		Applications/Databases
Url:		https://greenplum.org
Source0:	https://github.com/greenplum-db/gpdb/archive/%{version}.tar.gz
# No checksum for source file
Patch0:		greenplum-5.0.0-orca-configure-use-cmake3.patch
BuildRequires:	apr-devel 
BuildRequires:	bison flex 
BuildRequires:	bzip2-devel 
BuildRequires:	cmake3 
BuildRequires:	devtoolset-6-gcc 
BuildRequires:	devtoolset-6-gcc-c++
BuildRequires:	 devtoolset-6-binutils 
BuildRequires:	krb5-devel 
BuildRequires:	libcurl-devel 
BuildRequires:	libevent-devel 
BuildRequires:	libkadm5 
BuildRequires:	libyaml-devel 
BuildRequires:	libxml2-devel 
BuildRequires:	perl-ExtUtils-Embed 
BuildRequires:	python-devel 
BuildRequires:	python-pip 
BuildRequires:	readline-devel 
BuildRequires:	xerces-c-devel 
BuildRequires:	zlib-devel
BuildRequires:	perl-Env 
BuildRequires:	perl-Data-Dumper
BuildRequires:	python2
BuildRequires:	make
BuildRequires:	openssl-devel

# ? BuildRequires: for python modules

%description
The greenplum-db package includes the programs needed to create
and run a Greenplum Database server, which will in turn allow 
you to create and maintain Greenplum databases.
The Greenplum Database (GPDB) is an advanced, fully featured, 
open source data warehouse. It provides powerful and rapid 
analytics on petabyte scale data volumes. Uniquely geared 
toward big data analytics, Greenplum Database is powered by 
the world's most advanced cost-based query optimizer delivering 
high analytical query performance on large data volumes.

%prep
%%setup -q
%setup -q -n gpdb-%{version}
%patch0
# TODO conan: raise Exception("CMake is not found.  Please ensure the CMake 3.1 or later is installed")

%build
cd depends
autoconf
## depends with top level
./configure --prefix=$RPM_BUILD_ROOT/usr/local/gpdb
make -j4
cd ..
LD_LIBRARY_PATH=${PWD}/depends/build/lib ./configure --prefix=/usr/local/gpdb \
    --with-libraries=${PWD}/depends/build/lib \
    --with-includes=${PWD}/depends/build/include
#make

%install
#%makeinstall_std -C build
#mkdir -p $RPM_BUILD_ROOT/usr/local/gpdb/lib/postgresql
make DESTDIR=$RPM_BUILD_ROOT install
#make install
cd depends
make install_local
cd ..
#ls -l $RPM_BUILD_ROOT/usr/lib/debug/usr/local/gpdb/lib/python/pygresql
#rm -f $RPM_BUILD_ROOT/usr/lib/debug/usr/local/gpdb/lib/python/pygresql/_pg.so.debug

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
/usr/local/gpdb/lib/libgpopt.so*
/usr/local/gpdb/lib/libgpos.so*
/usr/local/gpdb/lib/libnaucrates.so*
/usr/local/gpdb/lib/libgpdbcost.so*
/usr/local/gpdb
