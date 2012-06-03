#!/usr/bin/perl
#
# A script to login to CPanel and modify a DNS record, automagically.
# Requires curl.

use strict;

my $CPANEL_USERNAME="user";
my $CPANEL_PASSWORD='password';
my $CPANEL_URL="http://cpanel.example.com";

# Get from CGI call.
my $IP="125.123.123.3";

my %JSON_VARS=(
  cpanel_jsonapi_version => 2,
  cpanel_jsonapi_module => "ZoneEdit",
  cpanel_jsonapi_func => "edit_zone_record",

  # These will values depend on your website.
  line => "29",
  domain => "example.com",
  name => "subdomain",
  ttl => "14400",
  type => "A",
  address => $IP
);

my $COOKIE_JAR="cookies.txt";

my $OPTS="-b $COOKIE_JAR -c $COOKIE_JAR";

my $JSON_API_CALL="json-api/cpanel?";

while (my ($key, $value) = each(%JSON_VARS)){
  $JSON_API_CALL=$JSON_API_CALL . "$key=$value&";
}

print `curl $OPTS -d 'user=$CPANEL_USERNAME' --data-urlencode 'pass=$CPANEL_PASSWORD' '$CPANEL_URL/login/'`;

print `curl $OPTS '$CPANEL_URL/$JSON_API_CALL'`;

