# env expansion in Bacula 9.x
env_fill() {
	local FILE=$1
	perl -pe 's!\${([^}]*)}!$ENV{$1}!g;' "$FILE"
}
