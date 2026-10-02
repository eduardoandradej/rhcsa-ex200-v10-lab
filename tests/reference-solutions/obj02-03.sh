#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
groupadd -g 33010 linuxops
groupadd auditteam
groupadd -g 33021 devtemp
groupmod -n devopsgrp devtemp
groupmod -g 33022 devopsgrp
groupadd oldgrp
groupdel oldgrp
EOS
