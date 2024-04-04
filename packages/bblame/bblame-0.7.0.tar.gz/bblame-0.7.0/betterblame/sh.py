"""Customize sh module after import"""
import sh

sh = sh.bake(_return_cmd=True)  # pylint: disable=E1101
