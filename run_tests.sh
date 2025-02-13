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

pytest "$@"