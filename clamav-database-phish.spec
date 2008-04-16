%define		database_version	20080416
%define		rel	0.2
Summary:	Phish database for clamav
Name:		clamav-database-phish
Version:	0.1
Release:	%{database_version}.%{rel}
License:	GPL
Group:		Applications/Databases
Source0:	 http://www.sanesecurity.com/clamav/scamsigs/phish.ndb.gz
# Source0-md5:	4ff089e09706b9212cd7b63a3b7e87ea
Source1:	http://www.sanesecurity.co.uk/clamav/phish_sigtest.txt
# Source1-md5:	d7a251c62cdd2f1b78a33476816447f3
URL:		http://www.sanesecurity.co.uk/clamav/
BuildRequires:	clamav
Requires:	clamav
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Phish database for ClamAV which will help detect some types of stock, lottery,
419 and some image spams that are around at the moment. (Updated
%{database_version}).

%prep
%setup -qcT
%{__gzip} -dc %{SOURCE0} > $(basename %{SOURCE0} .gz)

%build
# test
res=$(clamscan %{SOURCE1} --database phish.ndb | head -n1 | sed -e 's,^.*: ,,')
if [ "$res" != "Html.Phishing.Sanesecurity.TestSig FOUND" ]; then
	: Scan test failed: [$res]
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/clamav
install *.ndb $RPM_BUILD_ROOT/var/lib/clamav

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(644,clamav,root) %verify(not md5 mtime size) /var/lib/clamav/*.ndb
