#!/usr/bin/perl
package SMS::Cellsynt;
our $VERSION = 0.1;
use strict;
use warnings;
use WWW::Curl::Easy;
use Carp;

=pod

=head1 SYNOPSIS

 $sms = SMS::Cellsynt->new(
 	username=>'foo',
	password=>'bar',
 );

=cut

sub new {
	my $class = shift;
	my $self = {
		uri => 'https://se-1.cellsynt.net/sms.php',
		origtype => 'alpha',
		orig => 'PidginSMS',
		ttl => 1800,
		debug => 0,
		@_,
	};
	$self->{curl} = new WWW::Curl::Easy;

	bless $self, $class;
	return $self;
}

sub send_sms {
	my $self = shift;
	my $param = {
		@_,
	};

	my $username = $self->{username};
	my $password = $self->{password};
	my $origtype = $self->{origtype};
	my $orig = $self->{orig};
	my $ttl = $self->{ttl}+time;
	my $uri = $self->{uri};
	my $text = _uri_encode($param->{text});

	my $req = "$uri?username=$username&password=$password".
	          "&destination=".$param->{to}."&text=$text".
		  "&expiry=$ttl&originatortype=$origtype&originator=$orig";

	if($self->{debug}) {
		print "$req\n";
		return 0;
	}
	
	my $body;

	open(my $curld, ">", \$body);
	$self->{curl}->setopt(CURLOPT_URL, $req);
	$self->{curl}->setopt(CURLOPT_WRITEDATA, \$curld);
	$self->{curl}->setopt(CURLOPT_FOLLOWLOCATION, 1);
	$self->{curl}->perform();
	close $curld;

	if($body=~/^Error:/) {
		croak($body);
	}
}

sub _uri_encode {
	my $text = shift;
	$text =~ s/([^A-Za-z0-9])/sprintf("%%%02X", ord($1))/seg;
	return $text;
}

1;
