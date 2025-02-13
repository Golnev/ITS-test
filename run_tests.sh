#!/bin/sh

set -a
if [ -f .env ]; then
  . ./.env
else
  echo ".env file is not found."
fi
set +a

echo "Before entering the details, please register on the website."

echo "Enter email (default: $MY_EMAIL): "
read -r input_email
echo "Enter password (default: $MY_PASS): "
read -r input_password

MY_EMAIL=${input_email:-$MY_EMAIL}
MY_PASS=${input_password:-$MY_PASS}

export MY_EMAIL
export MY_PASS

echo "Enter the pytest marker if any('auth': for login and logout tests, 'users': for users tests, 'contacts' for contacts tests, 'negative' for negative tests): "
read -r marker

echo "Enter parser parameters if any('--rm' for deleting old data): "
read -r parser_params

command="pytest"
if [ -n "$marker" ]; then
  command="$command -m $marker"
fi

if [ -n "$parser_params" ]; then
  command="$command $parser_params"
fi

exec $command "$@"