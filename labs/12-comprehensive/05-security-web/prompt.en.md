Publish `/srv/secure12` through Apache on TCP 48890 while keeping SELinux
enforcing. Persist the file context, label the nonstandard HTTP port, open
the port persistently in the active firewalld zone, enable/start httpd, and
save state evidence.
