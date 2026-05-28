use strict;
use warnings;

use Test::More;
use JSON::PP qw(decode_json);

use lib 'challenge-4/lib';
use lib 'lib';

use DataSec::Classifier;

subtest 'builds a classification request' => sub {
    my $captured_body;

    my $classifier = DataSec::Classifier->new(
        api_key => 'test-key',
        model   => 'test-model',
        http_post => sub {
            my ($endpoint, $headers, $body) = @_;
            $captured_body = $body;

            is(
                $endpoint,
                'https://openrouter.ai/api/v1/chat/completions',
                'uses default OpenRouter endpoint',
            );
            is($headers->{Authorization}, 'Bearer test-key', 'sets auth header');

            return {
                choices => [
                    {
                        message => {
                            content => '{"sensitivity":"restricted","category":"credential","risk":"critical","reason":"Contains a password."}',
                        },
                    },
                ],
            };
        },
    );

    my $result = $classifier->classify('password=secret');
    my $payload = decode_json($captured_body);

    is($payload->{model}, 'test-model', 'uses configured model');
    is($payload->{temperature}, 0, 'uses deterministic temperature');
    is(ref $payload->{messages}, 'ARRAY', 'sends chat messages');
    is($result->{category}, 'credential', 'parses category');
    is($result->{risk}, 'critical', 'parses risk');
};

subtest 'extracts json from markdown fenced content' => sub {
    my $classifier = DataSec::Classifier->new(
        api_key => 'test-key',
        http_post => sub {
            return {
                choices => [
                    {
                        message => {
                            content => <<'JSON',
```json
{
  "sensitivity": "confidential",
  "category": "personal_data",
  "risk": "high",
  "reason": "Contains personal contact details."
}
```
JSON
                        },
                    },
                ],
            };
        },
    );

    my $result = $classifier->classify('ana@example.com');

    is($result->{sensitivity}, 'confidential', 'parses sensitivity');
    is($result->{category}, 'personal_data', 'parses category');
    is($result->{risk}, 'high', 'parses risk');
};

subtest 'requires all output fields' => sub {
    my $classifier = DataSec::Classifier->new(
        api_key => 'test-key',
        http_post => sub {
            return {
                choices => [
                    {
                        message => {
                            content => '{"sensitivity":"public"}',
                        },
                    },
                ],
            };
        },
    );

    eval { $classifier->classify('hello') };

    like($@, qr/missing field 'category'/, 'fails on incomplete JSON');
};

subtest 'requires api key and text' => sub {
    my $missing_key = DataSec::Classifier->new(api_key => '');
    eval { $missing_key->classify('hello') };
    like($@, qr/API key is required/, 'requires api key');

    my $missing_text = DataSec::Classifier->new(api_key => 'test-key');
    eval { $missing_text->classify('') };
    like($@, qr/Text sample is required/, 'requires text');
};

done_testing();
