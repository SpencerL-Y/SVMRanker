#!/usr/bin/perl

# /opt/local/bin/perl

use v5.12;
use autodie;


my $example = 0;
my $template;
my @usedTemplates = (0,0,0,0,0,0,0,0);

print "example,template\n";
for ($example = 0; $example < 172; $example++) {
	my $logfile = "$example.bpl.log";
	$template = "S";
	if ( -e -s $logfile ) {
		open(RESULT, $logfile);
		while (<RESULT>) {
			if ($_ =~ /------Using Template ([1234567890.]+) -----------/) {
				$template = $1;
			}
			if ($_ =~ /^FINATE/) {
				print "$example,$template\n";
				$usedTemplates[$template]++;
			}
		}
		close(RESULT);
	}
}
print "@usedTemplates ";
