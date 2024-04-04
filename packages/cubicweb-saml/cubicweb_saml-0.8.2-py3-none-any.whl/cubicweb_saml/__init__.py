# copyright 2019-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging

logger = logging.getLogger(__name__)


def includeme(config):
    """Activate the SAML authenticate cube"""
    from cubicweb_saml.pconfig import SAMLAuthenticationPolicy

    if config.registry.get("cubicweb.authpolicy") is None:
        raise ValueError(
            "saml: the default cubicweb auth policy should be "
            "available via the 'cubicweb.authpolicy' registry "
            "config entry"
        )

    cubicweb_sources = config.registry["cubicweb.config"].read_sources_file()

    if "saml" not in cubicweb_sources:
        logger.warning("saml: 'saml' section is missing in cubicweb sources file")

    elif "saml-metadata-uri" not in cubicweb_sources["saml"]:
        logger.warning("saml: 'saml-metadata-uri' option is missing")

    elif not cubicweb_sources["saml"]["saml-metadata-uri"]:
        logger.warning("saml: 'saml-metadata-uri' option is empty")

    else:
        settings = config.get_settings()
        authtkt_prefix = "cubicweb.auth.authtkt.session"
        defaults_settings = {
            "hashalg": settings.get(f"{authtkt_prefix}.hashalg", "sha512"),
            "cookie_name": settings.get(f"{authtkt_prefix}.cookie_name", "auth_tkt"),
            "timeout": settings.get(f"{authtkt_prefix}.timeout", 1200),
            "reissue_time": settings.get(f"{authtkt_prefix}.reissue_time", 120),
            "http_only": settings.get(f"{authtkt_prefix}.http_only", True),
            "secure": settings.get(f"{authtkt_prefix}.secure", True),
        }

        policy = SAMLAuthenticationPolicy(
            settings.get("cubicweb.auth.authtkt.session.secret"),
            settings.get("cubicweb.auth.authtkt.persistent.secret", "notsosecret"),
            defaults=defaults_settings,
        )

        config.registry["cubicweb.authpolicy"]._policies.append(policy)

        config.add_route("saml", "/saml")
        config.scan("cubicweb_saml.pconfig")
