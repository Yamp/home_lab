use strict;
use warnings;
use diagnostics;

use feature 'say';

use feature "switch";

use v5.22;

print "Hello world\n";


my $name = "Dmitriy";
my ($age, $street) = (40, '123 Main st');

my $my_info = "$name lives on \"$street\"\n";
$my_info = qq{$name lives on "$street"\n};

print $my_info;

my $multiline = <<"END";
This is
a bunch
of long
long shit
END

say $multilineжт
