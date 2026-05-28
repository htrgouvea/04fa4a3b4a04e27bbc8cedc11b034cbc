#!/usr/bin/env perl

use strict;
use warnings;

use FindBin qw($Bin);
use Getopt::Long qw(GetOptions);
use lib "$Bin/../lib";

use DataSec::Classifier;

my $text;
my $file;
my $endpoint;
my $model;
my $help;

GetOptions(
    'text=s'     => \$text,
    'file=s'     => \$file,
    'endpoint=s' => \$endpoint,
    'model=s'    => \$model,
    'help'       => \$help,
) or _usage(1);

_usage(0) if $help;

if (defined $file) {
    open my $fh, '<', $file or die "Could not open '$file': $!\n";
    local $/;
    $text = <$fh>;
    close $fh;
}

if (!defined $text) {
    local $/;
    $text = <STDIN>;
}

my $classifier = DataSec::Classifier->new(
    endpoint => $endpoint,
    model    => $model,
);

my $classification = $classifier->classify($text);
print $classifier->encode_pretty_json($classification);

sub _usage {
    my ($exit_code) = @_;

    print <<'USAGE';
Usage:
  OPENROUTER_API_KEY=... perl bin/classify_text.pl --text "password=123"
  OPENROUTER_API_KEY=... perl bin/classify_text.pl --file sample.txt
  echo "john@example.com" | OPENROUTER_API_KEY=... perl bin/classify_text.pl

Options:
  --text       Text sample to classify.
  --file       File containing the text sample.
  --endpoint   OpenAI-compatible chat completions endpoint.
               Default: https://openrouter.ai/api/v1/chat/completions
  --model      Model name.
               Default: openai/gpt-4o-mini
  --help       Show this help message.

Environment:
  OPENROUTER_API_KEY              Required API key.
  OPENAI_API_KEY                  Alternative API key variable.
  CLASSIFIER_MODEL                Optional default model.
  OPENAI_COMPATIBLE_ENDPOINT      Optional default endpoint.
  OPENROUTER_SITE_URL             Optional OpenRouter attribution header.
  OPENROUTER_APP_NAME             Optional OpenRouter attribution header.
USAGE

    exit $exit_code;
}
