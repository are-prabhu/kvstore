# kvstore

kvstore is a basic key value store developed using flask and sqlite3 db.


# DEPLOYMENT

To Deploy kvstore follow the given steps

```
apt-get install -y ansible
git clone git@github.com:are-prabhu/kvstore.git
cd kvstore/deployment
```
kvstore can be deployed using ansible scripts, 
change the ansible variables to point the requirements.txt (https://github.com/are-prabhu/kvstore/blob/master/deployment/deploy-kv/vars/main.yml)

Run the following commant to deploy the kvstore

```
ansible-playbook -s deploy-kv/Playbook.yml
```


# CLIENT USAGE

usage: kvstore-client.sh [-get] | [-put] | [-watch]
Example: 

To Put a value 
```
kvstore-client.sh -put foo bar 
```

To Get a value 
```
kvstore-client.sh -get foo 
```

To Get a value 
```
kvstore-client.sh -watch 
```
