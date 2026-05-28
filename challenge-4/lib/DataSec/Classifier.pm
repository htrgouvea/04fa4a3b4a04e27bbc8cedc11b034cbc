package DataSec::Classifier;

use strict;
use warnings;

use HTTP::Tiny;
use JSON::PP qw(decode_json encode_json);

our $VERSION = '1.0.0';

my $DEFAULT_ENDPOINT = 'https://openrouter.ai/api/v1/chat/completions';
my $DEFAULT_MODEL    = 'openai/gpt-4o-mini';

sub new {
    my ($class, %args) = @_;

    my $self = {
        api_key  => $args{api_key}  || $ENV{OPENROUTER_API_KEY}
            || $ENV{OPENAI_API_KEY},
        endpoint => $args{endpoint} || $ENV{OPENAI_COMPATIBLE_ENDPOINT}
            || $DEFAULT_ENDPOINT,
        model => $args{model} || $ENV{CLASSIFIER_MODEL} || $DEFAULT_MODEL,
        site_url   => $args{site_url}   || $ENV{OPENROUTER_SITE_URL},
        app_name   => $args{app_name}   || $ENV{OPENROUTER_APP_NAME},
        http_post  => $args{http_post},
        json_codec => JSON::PP->new->utf8->canonical,
    };

    bless $self, $class;
    return $self;
}

sub classify {
    my ($self, $text) = @_;

    die "Text sample is required\n" if !defined $text || $text eq '';
    die "API key is required. Set OPENROUTER_API_KEY or OPENAI_API_KEY.\n"
        if !$self->{api_key};

    my $response = $self->_post_chat_completion($text);
    my $content  = $self->_extract_message_content($response);

    return $self->_parse_classification_json($content);
}

sub build_messages {
    my ($self, $text) = @_;

    return [
        {
            role    => 'system',
            content => join "\n",
                'You are a data security classification engine.',
                'Classify short text samples for sensitivity, category, and risk.',
                'Return only valid JSON. Do not use Markdown.',
                'Use this schema:',
                '{',
                '  "sensitivity": "public|internal|confidential|restricted",',
                '  "category": "credential|personal_data|financial|health|legal|security|business|other",',
                '  "risk": "low|medium|high|critical",',
                '  "reason": "short explanation"',
                '}',
        },
        {
            role    => 'user',
            content => "Classify this text sample:\n\n$text",
        },
    ];
}

sub _post_chat_completion {
    my ($self, $text) = @_;

    my $payload = {
        model       => $self->{model},
        temperature => 0,
        messages    => $self->build_messages($text),
    };

    my $headers = {
        'Authorization' => "Bearer $self->{api_key}",
        'Content-Type'  => 'application/json',
    };

    # OpenRouter accepts these optional headers for dashboard attribution.
    $headers->{'HTTP-Referer'} = $self->{site_url} if $self->{site_url};
    $headers->{'X-Title'}      = $self->{app_name} if $self->{app_name};

    my $body = $self->{json_codec}->encode($payload);

    if ($self->{http_post}) {
        return $self->{http_post}->($self->{endpoint}, $headers, $body);
    }

    my $http = HTTP::Tiny->new(timeout => 30);
    my $raw_response = $http->post(
        $self->{endpoint},
        {
            headers => $headers,
            content => $body,
        },
    );

    if (!$raw_response->{success}) {
        my $status = $raw_response->{status} || 'unknown';
        my $reason = $raw_response->{reason} || 'request failed';
        die "LLM request failed: HTTP $status $reason\n";
    }

    return decode_json($raw_response->{content});
}

sub _extract_message_content {
    my ($self, $response) = @_;

    my $choices = $response->{choices};
    die "LLM response did not include choices\n"
        if ref $choices ne 'ARRAY' || !@$choices;

    my $content = $choices->[0]{message}{content};
    die "LLM response did not include message content\n"
        if !defined $content || $content eq '';

    return $content;
}

sub _parse_classification_json {
    my ($self, $content) = @_;

    my $json_text = _extract_json_object($content);
    my $result = eval { decode_json($json_text) };
    die "Could not parse LLM JSON response: $@\nRaw content:\n$content\n" if $@;

    for my $field (qw(sensitivity category risk reason)) {
        die "LLM JSON response missing field '$field'\n"
            if !exists $result->{$field};
    }

    return {
        sensitivity => $result->{sensitivity},
        category    => $result->{category},
        risk        => $result->{risk},
        reason      => $result->{reason},
    };
}

sub _extract_json_object {
    my ($content) = @_;

    $content =~ s/\A\s+|\s+\z//g;

    # Some models wrap JSON in Markdown fences even when asked not to.
    $content =~ s/\A```(?:json)?\s*//i;
    $content =~ s/\s*```\z//;
    $content =~ s/\A\s+|\s+\z//g;

    if ($content =~ /(\{.*\})/s) {
        return $1;
    }

    return $content;
}

sub encode_pretty_json {
    my ($self, $data) = @_;
    return JSON::PP->new->utf8->canonical->pretty->encode($data);
}

1;
