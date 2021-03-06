package FS::Mason::Request;

use strict;
use warnings;
use vars qw( $FSURL $QUERY_STRING );
use base 'HTML::Mason::Request';

$FSURL = 'http://Set/FS_Mason_Request_FSURL/in_standalone_mode/';
$QUERY_STRING = '';

sub new {
    my $class = shift;

    my $superclass = $HTML::Mason::ApacheHandler::VERSION ?
                     'HTML::Mason::Request::ApacheHandler' :
                     $HTML::Mason::CGIHandler::VERSION ?
                     'HTML::Mason::Request::CGI' :
                     'HTML::Mason::Request';

    $class->alter_superclass( $superclass );

    #huh... shouldn't alter_superclass take care of this for us?
    __PACKAGE__->valid_params( %{ $superclass->valid_params() } );

    my %opt = @_;
    my $mode = $superclass =~ /Apache/i ? 'apache' : 'standalone';
    $class->freeside_setup($opt{'comp'}, $mode);

    $class->SUPER::new(@_);

}

#override alter_superclass ala RT::Interface::Web::Request ??
# for Mason 1.39 vs. Perl 5.10.0

my $protect_fds;

sub freeside_setup {
    my( $class, $filename, $mode ) = @_;

    #from rt/bin/webmux.pl(.in)
    if ( !$protect_fds && $ENV{'MOD_PERL'} && exists $ENV{'MOD_PERL_API_VERSION'}
        && $ENV{'MOD_PERL_API_VERSION'} >= 2
    ) {
        # under mod_perl2, STDIN and STDOUT get closed and re-opened,
        # however they are not on FD 0 and 1.  In this case, the next
        # socket that gets opened will occupy one of these FDs, and make
        # all system() and open "|-" calls dangerous; for example, the
        # DBI handle can get this FD, which later system() calls will
        # close by putting garbage into the socket.
        $protect_fds = [];
        push @{$protect_fds}, IO::Handle->new_from_fd(0, "r")
            if fileno(STDIN) != 0;
        push @{$protect_fds}, IO::Handle->new_from_fd(1, "w")
            if fileno(STDOUT) != 1;
    }

    if ( $filename =~ qr(/REST/\d+\.\d+/NoAuth/) ) {

      package HTML::Mason::Commands; #?
      use FS::UID qw( adminsuidsetup );

      #need to log somebody in for the mail gw

      ##old installs w/fs_selfs or selfserv??
      #&adminsuidsetup('fs_selfservice');

      &adminsuidsetup('fs_queue');

    } else {

      package HTML::Mason::Commands;
      use vars qw( $cgi $p $fsurl ); # $lh ); #not using /mt
      use Encode;
      use FS::UID qw( cgisuidsetup );
      use FS::CGI qw( popurl rooturl );

      if ( $mode eq 'apache' ) {
        $cgi = new CGI;
        &cgisuidsetup($cgi);
        #&cgisuidsetup($r);
        $fsurl = rooturl();
        $p = popurl(2);
      } elsif ( $mode eq 'standalone' ) {
        $cgi = new CGI $FS::Mason::Request::QUERY_STRING; #better keep setting
                                                          #if you set it once
        $FS::UID::cgi = $cgi;
        $fsurl = $FS::Mason::Request::FSURL; #kludgy, but what the hell
        $p = popurl(2, "$fsurl$filename");
      } else {
        die "unknown mode $mode";
      }

    #
    foreach my $param ( $cgi->param ) {
      my @values = $cgi->param($param);
      next if $cgi->uploadInfo($values[0]);
      #warn $param;
      @values = map decode(utf8=>$_), @values;
      $cgi->param($param, @values);
    }
    
  }

}

sub callback {
  RT::Interface::Web::Request::callback(@_);
}

sub request_path {
  RT::Interface::Web::Request::request_path(@_);
}

1;
