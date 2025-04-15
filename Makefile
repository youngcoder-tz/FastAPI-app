init-locales:
	echo "Initializing locale files..."
	./generate_locales.sh
	echo "Locales ready in locales/"

update-translations:
	xgettext -d messages -o locales/messages.pot app/**/*.py --from-code=UTF-8
	echo "Translation template updated"

compile-translations:
	for lang in en sw fr; do \
		msgfmt locales/$$lang/LC_MESSAGES/ui.po -o locales/$$lang/LC_MESSAGES/ui.mo; \
	done
	echo "Translations compiled to binary format"
