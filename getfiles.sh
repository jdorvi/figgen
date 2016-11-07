readPassword () {
  echo Ssh Password: 
  read -s SSHPASS
  eval "export SSHPASS='""$SSHPASS""'"
}

# read password

readPassword

# declare list of storms as array
declare -a directories=("OS1_Exit_0010_007" "OS1_Exit_0010_008" "OS1_Exit_0010_009")
declare -a files=("fort.63.bz2" "fort.73.bz2" "fort.74.bz2" "rads.64.bz2" "swan_DIR.63.bz2" "swan_HS.63.bz2" "swan_TMM10.63.bz2" "swan_TPS.63.bz2")
declare remote_root="dorvinen@login1.corral.tacc.utexas.edu:/gpfs/corral3/repl/projects/RIVAECOM/wfl/Prod/runsv8/trop"
for dir in "${directories[@]}"
do
  # create directory variables	
  remote_dir="$remote_root/$dir"
  local_dir="/media/sf_P_DRIVE/04/QC/Tropical_Released09152016_large/$dir"
  # check if local_dir exists and create it if not
  if [ ! -d "$local_dir" ]; then 
    mkdir $local_dir
  fi	

	for filed in "${files[@]}"
	do
    remote_file="$remote_dir/$filed"
    local_file="$local_dir/$file"
    echo "copying $dir/$filed"
    sshpass -e  scp $remote_file $local_file
	done
done
