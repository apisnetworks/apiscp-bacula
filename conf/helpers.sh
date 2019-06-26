# env expansion in Bacula 9.x
env_fill() {
	local FILE=$1
	perl -pe 's!\${([^}]*)}!$ENV{$1}!g;' "$FILE"
}

# Pull local.d or conf.d
flexible_check() {
	BACULAHOME="/etc/bacula"
	for BASE in local.d conf.d; do
		[[ ! -f "$BACULAHOME/$BASE/$1" ]] && continue
		echo "$BACULAHOME/$BASE/$1"
		return
	done
	>&2 echo "FAILED TO LOCATE $1"
	exit 1
}
