def call(Map params = [
            package_name: ""
            fileslist: "files.txt", 
            rootdir: "",
            ssh_credentials_id: "ssh_credentials",
            data_dir = 'sca-data';
            ssh_host = 'localhost';
        ]) {
    script {
        if (params.package_name == "") {
            throw new Exception("package_name is required");
        }
        if (params.rootdir == "") {
            throw new Exception("fileslist is required");
        }
        echo params

        files = readFile(params.fileslist).split("\n")

        withCredentials(bindings: [sshUserPrivateKey(credentialsId: params.ssh_credentials_id, \
                                            keyFileVariable: 'SSH_KEY', \
                                            passphraseVariable: '', \
                                            usernameVariable: 'SSH_USER')]) {
                    
            // create a directory:
            sh 'ssh -i ${SSH_KEY} ${SSH_USER}@${params.ssh_host} "mkdir -p ${params.data_dir}/${params.package_name}/source"'

            // use scp to push the artifacts
            
            for(file in files) {
                absolute_file = rootdir + "/" + file 
                sh 'scp -i ${SSH_KEY} ${absolute_file} ${SSH_USER}@${params.ssh_host}:${params.data_dir}/${params.package_name}/source/${file}'
            }
        }
    }
}