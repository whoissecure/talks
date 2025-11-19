#!/usr/bin/perl
use strict;
use warnings;
use Mojolicious::Lite;
use JSON;

my %wallets = (
    daniel => 30,
    miquel => 30,
    rooted => 30,
);

my $PRODUCT_PRICE = 20;

post '/wallet' => sub {
    my $c = shift;
    my $json_input = $c->req->body;
    my $data;

    eval {
        $data = decode_json($json_input);
        1;
    } or do {
        my $error = $@ || 'Unknown error';
        return $c->render(status => 400, json => { error => "Invalid JSON: $error" });
    };

    my $user = $data->{'user'} // return $c->render(status => 400, json => { error => "Parameter not received: 'user'" });

    unless (exists $wallets{$user}) {
        return $c->render(status => 404, json => { error => "User not found" });
    }

    $c->render(json => { user => $user, balance => $wallets{$user} });
};

post '/buy' => sub {
    my $c = shift;
    my $json_input = $c->req->body;
    my $data;

    eval {
        $data = decode_json($json_input);
        1;
    } or do {
        my $error = $@ || 'Unknown error';
        return $c->render(status => 400, json => { error => "Invalid JSON: $error" });
    };

    my $user = $data->{'user'} // return $c->render(status => 400, json => { error => "Parameter not received: 'user'" });
    my $quantity = $data->{'quantity'} // return $c->render(status => 400, json => { error => "Parameter not received: 'quantity'" });

    unless (exists $wallets{$user}) {
        return $c->render(status => 404, json => { error => "User not found" });
    }

    my $total = $PRODUCT_PRICE * $quantity;
    my $new_balance = $wallets{$user} - $total;

    if ($new_balance < 0) {
        return $c->render(json => { error => "Balance is not enough", attempted_balance => $new_balance });
    } else {
        $wallets{$user} = $new_balance;
        return $c->render(json => { msg => "Product successfully bought", balance_restante => $wallets{$user} });
    }
};

app->start;
