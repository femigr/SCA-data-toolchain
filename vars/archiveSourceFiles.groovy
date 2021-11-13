def call(Map params = [
            package_name: "",
            fileslist: "files.txt", 
            ssh_credentials_id: "ssh_credentials",
            data_dir: 'sca-data',
            ssh_host: 'localhost',
            state: 'old' // old or new
        ]) {
    script { 
        echo params.toString()

        files = readFile(params.fileslist).split("\n")
        echo files.toString()

        withCredentials(bindings: [sshUserPrivateKey(credentialsId: params.ssh_credentials_id, \
                                            keyFileVariable: 'SSH_KEY', \
                                            passphraseVariable: '', \
                                            usernameVariable: 'SSH_USER')]) {
                    
            // create a directory:
            sh 'ssh -i ${SSH_KEY} ${SSH_USER}@' + params.ssh_host + ' "mkdir -p ' + params.data_dir + '/' + params.package_name + '/source/' + params.state + '"'

            // use scp to push the artifacts
            dir(params.state + '/' + params.package_name){ 
                for(file in files) {
                    try{
                        sh 'rsync -R -e "ssh -i ${SSH_KEY}" ' + file + ' ${SSH_USER}@' + params.ssh_host + ':' + params.data_dir + '/' + params.package_name + '/source/' + params.state + '/'
                    } catch(e) {
                        echo 'error: ' + e.toString()
                    }
                }
            }
        }
    }
}