#!/bin/bash
echo "Creating locale directories..."
for lang in en sw fr; do
    mkdir -p "locales/$lang/LC_MESSAGES"
    echo "Generating $lang translation file..."
    msginit -i locales/messages.pot -o "locales/$lang/LC_MESSAGES/ui.po" -l "$lang" --no-translator
done
echo "Basic translation files created in locales/"
