#!/usr/bin/perl

# /opt/local/bin/perl

use v5.12;
use autodie;


my $example = 0;
my $time_sampling = 0.0;
my $time_training = 0.0;
my $time_Z3 = 0.0;
my $result;
my $phase;

print "example,time_sampling,time_training,time_Z3,result,lastPhase\n";
my ($path) = @ARGV;
my @files = glob(@_[0]);
foreach(@files) {
	if(-d $_){
		print $_;
	} else {
	my $logfile = "$_.bpl.log";
	$time_sampling = 0.0;
	$time_training = 0.0;
	$time_Z3 = 0.0;
	$result = "T";
	$phase = "S";
	if ( -e -s $logfile ) {
		open(RESULT, $logfile);
		while (<RESULT>) {
			if ($_ =~ /sampling time = ([1234567890.]+) ms/) {
				$time_sampling = $time_sampling + $1;
			}
			if ($_ =~ /train_ranking_functioning time = ([1234567890.]+) ms/) {
				$time_training = $time_training + $1;
			}
			if ($_ =~ /verifying time = ([1234567890.]+) ms/) {
				$time_Z3 = $time_Z3 + $1;
			}
			if ($_ =~ /FINATE/) {
				$result = "Y";
			}
			if ($_ =~ /INFINATE/) {
				$result = "N";
			}
			if ($_ =~ /sampling time = ([1234567890.]+) ms/) {
				$phase = "T";
			}
			if ($_ =~ /[0-9 ->]* End train ranking function/) {
				$phase = "V";
			}
			if ($_ =~ /[0-9 ->]* End verify ranking function/) {
				$phase = "S";
			}
		}
		close(RESULT);
		print "$example,$time_sampling,$time_training,$time_Z3,$result,$phase\n";
	}
	}
}
