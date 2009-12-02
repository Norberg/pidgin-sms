#!/usr/bin/perl
# Copyright 2009, Olof Johansson <zibri@ethup.se>
use strict;
use warnings;
our $VERSION='1.0';
use SMS::Cellsynt;
use Getopt::Std;

sub HELP_MESSAGE {
	print "cellsynt.pl <flags>\n\n";
	print " -u <username>\n";
	print " -p <password>\n";
	print " -m <message>\n";
	print " -r <receiver>\n";
	print " -O <alpha|number|shortcode>\n";
	print " -o <originator (format depends on -O>\n";
	print " -d <debug>\n";
	exit;
}

our($opt_u,$opt_p,$opt_m,$opt_r,$opt_o,$opt_O,$opt_d);
getopts('u:p:m:r:o:O:d');

if(!defined $opt_u) {
	print STDERR "No username specified\n";
	HELP_MESSAGE();
	exit 1;
}

if(!defined $opt_p) {
	print STDERR "No password specified\n";
	HELP_MESSAGE();
	exit 1;
}

if(!defined $opt_m) {
	print STDERR "No message specified\n";
	HELP_MESSAGE();
	exit 1;
}

if(!defined $opt_r) {
	print STDERR "No receiver specified\n";
	HELP_MESSAGE();
	exit 1;
}

if(!defined $opt_O) {
	print STDERR "No originator type specified\n";
	HELP_MESSAGE();
	exit 1;
}

if(!defined $opt_o) {
	print STDERR "No orignator specified\n";
	HELP_MESSAGE();
	exit 1;
}

my $debug=$opt_d?1:0;
my $msg = substr($opt_m, 0, 160);

my $num=$opt_r;

unless($num =~ /^(?:0046|\+46|0)(?:10|7[0236]|74[123457])/) {
	die("Not a Swedish cell phone number");
}

unless($num =~ /^0046/) {
	$num=~s/^\+46/0046/ or $num=~s/^0/0046/;
}

my $sms = SMS::Cellsynt->new(
	username=>$opt_u,
	password=>$opt_p,
	origtype=>$opt_O,
	orig=>$opt_o,
	debug=>$debug,
);

$sms->send_sms(
	text=>$msg,
	to=>$num,
);

