import uuid
import xml.etree.ElementTree as ET
from mock import patch

open_shell_request = """\
<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:cfg="http://schemas.microsoft.com/wbem/wsman/1/config" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:n="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:env="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
  <env:Header>
    <a:To>http://windows-host:5985/wsman</a:To>
    <a:ReplyTo>
      <a:Address mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
    </a:ReplyTo>
    <w:MaxEnvelopeSize mustUnderstand="true">153600</w:MaxEnvelopeSize>
    <a:MessageID>uuid:11111111-1111-1111-1111-111111111111</a:MessageID>
    <w:Locale mustUnderstand="false" xml:lang="en-US" />
    <p:DataLocale mustUnderstand="false" xml:lang="en-US" />
    <w:OperationTimeout>PT60S</w:OperationTimeout>
    <w:ResourceURI mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
    <a:Action mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/transfer/Create</a:Action>
    <w:OptionSet>
      <w:Option Name="WINRS_NOPROFILE">FALSE</w:Option>
      <w:Option Name="WINRS_CODEPAGE">437</w:Option>
    </w:OptionSet>
  </env:Header>
  <env:Body>
    <rsp:Shell>
      <rsp:InputStreams>stdin</rsp:InputStreams>
      <rsp:OutputStreams>stdout stderr</rsp:OutputStreams>
    </rsp:Shell>
  </env:Body>
</env:Envelope>"""

open_shell_response = """\
<?xml version="1.0" ?>
<s:Envelope xml:lang="en-US" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer">
	<s:Header>
		<a:Action>http://schemas.xmlsoap.org/ws/2004/09/transfer/CreateResponse</a:Action>
		<a:MessageID>uuid:11111111-1111-1111-1111-111111111112</a:MessageID>
		<a:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:To>
		<a:RelatesTo>uuid:11111111-1111-1111-1111-111111111111</a:RelatesTo>
	</s:Header>
	<s:Body>
		<x:ResourceCreated>
			<a:Address>http://windows-host:5985/wsman</a:Address>
			<a:ReferenceParameters>
				<w:ResourceURI>http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
				<w:SelectorSet>
					<w:Selector Name="ShellId">11111111-1111-1111-1111-111111111113</w:Selector>
				</w:SelectorSet>
			</a:ReferenceParameters>
		</x:ResourceCreated>
	</s:Body>
</s:Envelope>"""

close_shell_request = """\
<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:cfg="http://schemas.microsoft.com/wbem/wsman/1/config" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:n="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:env="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
  <env:Header>
    <a:To>http://windows-host:5985/wsman</a:To>
    <a:ReplyTo>
      <a:Address mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
    </a:ReplyTo>
    <w:MaxEnvelopeSize mustUnderstand="true">153600</w:MaxEnvelopeSize>
    <a:MessageID>uuid:11111111-1111-1111-1111-111111111111</a:MessageID>
    <w:Locale mustUnderstand="false" xml:lang="en-US" />
    <p:DataLocale mustUnderstand="false" xml:lang="en-US" />
    <w:OperationTimeout>PT60S</w:OperationTimeout>
    <w:ResourceURI mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
    <a:Action mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/09/transfer/Delete</a:Action>
    <w:SelectorSet>
      <w:Selector Name="ShellId">11111111-1111-1111-1111-111111111113</w:Selector>
    </w:SelectorSet>
  </env:Header>
  <env:Body>
  </env:Body>
</env:Envelope>"""

close_shell_response = """\
<?xml version="1.0" ?>
<s:Envelope xml:lang="en-US" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd">
	<s:Header>
		<a:Action>http://schemas.xmlsoap.org/ws/2004/09/transfer/DeleteResponse</a:Action>
		<a:MessageID>uuid:11111111-1111-1111-1111-111111111112</a:MessageID>
		<a:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:To>
		<a:RelatesTo>uuid:11111111-1111-1111-1111-111111111111</a:RelatesTo>
	</s:Header>
	<s:Body/>
</s:Envelope>
"""

run_cmd_with_args_request = """\
<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:cfg="http://schemas.microsoft.com/wbem/wsman/1/config" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:n="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:env="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
  <env:Header>
    <a:To>http://windows-host:5985/wsman</a:To>
    <a:ReplyTo>
      <a:Address mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
    </a:ReplyTo>
    <w:MaxEnvelopeSize mustUnderstand="true">153600</w:MaxEnvelopeSize>
    <a:MessageID>uuid:11111111-1111-1111-1111-111111111111</a:MessageID>
    <w:Locale mustUnderstand="false" xml:lang="en-US" />
    <p:DataLocale mustUnderstand="false" xml:lang="en-US" />
    <w:OperationTimeout>PT60S</w:OperationTimeout>
    <w:ResourceURI mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
    <a:Action mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command</a:Action>
    <w:SelectorSet>
      <w:Selector Name="ShellId">11111111-1111-1111-1111-111111111113</w:Selector>
    </w:SelectorSet>
    <w:OptionSet>
      <w:Option Name="WINRS_CONSOLEMODE_STDIN">TRUE</w:Option>
      <w:Option Name="WINRS_SKIP_CMD_SHELL">FALSE</w:Option>
    </w:OptionSet>
  </env:Header>
  <env:Body>
    <rsp:CommandLine>
      <rsp:Command>ipconfig</rsp:Command>
      <rsp:Arguments>/all</rsp:Arguments>
    </rsp:CommandLine>
  </env:Body>
</env:Envelope>"""

run_cmd_wo_args_request = """\
<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:cfg="http://schemas.microsoft.com/wbem/wsman/1/config" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:n="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:env="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
  <env:Header>
    <a:To>http://windows-host:5985/wsman</a:To>
    <a:ReplyTo>
      <a:Address mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
    </a:ReplyTo>
    <w:MaxEnvelopeSize mustUnderstand="true">153600</w:MaxEnvelopeSize>
    <a:MessageID>uuid:11111111-1111-1111-1111-111111111111</a:MessageID>
    <w:Locale mustUnderstand="false" xml:lang="en-US" />
    <p:DataLocale mustUnderstand="false" xml:lang="en-US" />
    <w:OperationTimeout>PT60S</w:OperationTimeout>
    <w:ResourceURI mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
    <a:Action mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command</a:Action>
    <w:SelectorSet>
      <w:Selector Name="ShellId">11111111-1111-1111-1111-111111111113</w:Selector>
    </w:SelectorSet>
    <w:OptionSet>
      <w:Option Name="WINRS_CONSOLEMODE_STDIN">TRUE</w:Option>
      <w:Option Name="WINRS_SKIP_CMD_SHELL">FALSE</w:Option>
    </w:OptionSet>
  </env:Header>
  <env:Body>
    <rsp:CommandLine>
      <rsp:Command>hostname</rsp:Command>
    </rsp:CommandLine>
  </env:Body>
</env:Envelope>"""

run_cmd_response = """\
<?xml version="1.0" ?>
<s:Envelope xml:lang="en-US" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer">
	<s:Header>
		<a:Action>http://schemas.microsoft.com/wbem/wsman/1/windows/shell/CommandResponse</a:Action>
		<a:MessageID>uuid:11111111-1111-1111-1111-111111111112</a:MessageID>
		<a:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:To>
		<a:RelatesTo>uuid:11111111-1111-1111-1111-111111111111</a:RelatesTo>
	</s:Header>
	<s:Body>
		<rsp:CommandResponse>
			<rsp:CommandId>11111111-1111-1111-1111-111111111114</rsp:CommandId>
		</rsp:CommandResponse>
	</s:Body>
</s:Envelope>"""

cleanup_cmd_request = """\
<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:cfg="http://schemas.microsoft.com/wbem/wsman/1/config" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:n="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:env="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
  <env:Header>
    <a:To>http://windows-host:5985/wsman</a:To>
    <a:ReplyTo>
      <a:Address mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
    </a:ReplyTo>
    <w:MaxEnvelopeSize mustUnderstand="true">153600</w:MaxEnvelopeSize>
    <a:MessageID>uuid:11111111-1111-1111-1111-111111111111</a:MessageID>
    <w:Locale mustUnderstand="false" xml:lang="en-US" />
    <p:DataLocale mustUnderstand="false" xml:lang="en-US" />
    <w:OperationTimeout>PT60S</w:OperationTimeout>
    <w:ResourceURI mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
    <a:Action mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Signal</a:Action>
    <w:SelectorSet>
      <w:Selector Name="ShellId">11111111-1111-1111-1111-111111111113</w:Selector>
    </w:SelectorSet>
  </env:Header>
  <env:Body>
    <rsp:Signal CommandId="11111111-1111-1111-1111-111111111114">
      <rsp:Code>http://schemas.microsoft.com/wbem/wsman/1/windows/shell/signal/terminate</rsp:Code>
    </rsp:Signal>
  </env:Body>
</env:Envelope>"""

cleanup_cmd_response = """\
<?xml version="1.0" ?>
<s:Envelope xml:lang="en-US" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer">
	<s:Header>
		<a:Action>http://schemas.microsoft.com/wbem/wsman/1/windows/shell/SignalResponse</a:Action>
		<a:MessageID>uuid:11111111-1111-1111-1111-111111111112</a:MessageID>
		<a:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:To>
		<a:RelatesTo>uuid:11111111-1111-1111-1111-111111111111</a:RelatesTo>
	</s:Header>
	<s:Body>
		<rsp:SignalResponse/>
	</s:Body>
</s:Envelope>"""

get_cmd_output_request = """\
<?xml version="1.0" encoding="utf-8"?>
<env:Envelope xmlns:x="http://schemas.xmlsoap.org/ws/2004/09/transfer" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd" xmlns:cfg="http://schemas.microsoft.com/wbem/wsman/1/config" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:n="http://schemas.xmlsoap.org/ws/2004/09/enumeration" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:env="http://www.w3.org/2003/05/soap-envelope" xmlns:b="http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing">
  <env:Header>
    <a:To>http://windows-host:5985/wsman</a:To>
    <a:ReplyTo>
      <a:Address mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
    </a:ReplyTo>
    <w:MaxEnvelopeSize mustUnderstand="true">153600</w:MaxEnvelopeSize>
    <a:MessageID>uuid:11111111-1111-1111-1111-111111111111</a:MessageID>
    <w:Locale mustUnderstand="false" xml:lang="en-US" />
    <p:DataLocale mustUnderstand="false" xml:lang="en-US" />
    <w:OperationTimeout>PT60S</w:OperationTimeout>
    <w:ResourceURI mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
    <a:Action mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Receive</a:Action>
    <w:SelectorSet>
      <w:Selector Name="ShellId">11111111-1111-1111-1111-111111111113</w:Selector>
    </w:SelectorSet>
  </env:Header>
  <env:Body>
    <rsp:Receive>
      <rsp:DesiredStream CommandId="11111111-1111-1111-1111-111111111114">stdout stderr</rsp:DesiredStream>
    </rsp:Receive>
  </env:Body>
</env:Envelope>"""

get_cmd_output_response = """\
<?xml version="1.0" ?>
<s:Envelope xml:lang="en-US" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:p="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd" xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell" xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd">
	<s:Header>
		<a:Action>http://schemas.microsoft.com/wbem/wsman/1/windows/shell/ReceiveResponse</a:Action>
		<a:MessageID>uuid:11111111-1111-1111-1111-111111111112</a:MessageID>
		<a:To>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:To>
		<a:RelatesTo>uuid:11111111-1111-1111-1111-111111111111</a:RelatesTo>
	</s:Header>
	<s:Body>
		<rsp:ReceiveResponse>
			<rsp:Stream CommandId="11111111-1111-1111-1111-111111111114" Name="stdout">DQpXaW5kb3dzIElQIENvbmZpZ3VyYXRpb24NCg0K</rsp:Stream>
			<rsp:Stream CommandId="11111111-1111-1111-1111-111111111114" Name="stdout">ICAgSG9zdCBOYW1lIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiAuIDogV0lORE9XUy1IT1NUCiAgIFByaW1hcnkgRG5zIFN1ZmZpeCAgLiAuIC4gLiAuIC4gLiA6IAogICBOb2RlIFR5cGUgLiAuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiBIeWJyaWQKICAgSVAgUm91dGluZyBFbmFibGVkLiAuIC4gLiAuIC4gLiAuIDogTm8KICAgV0lOUyBQcm94eSBFbmFibGVkLiAuIC4gLiAuIC4gLiAuIDogTm8KCkV0aGVybmV0IGFkYXB0ZXIgTG9jYWwgQXJlYSBDb25uZWN0aW9uOgoKICAgQ29ubmVjdGlvbi1zcGVjaWZpYyBETlMgU3VmZml4ICAuIDogCiAgIERlc2NyaXB0aW9uIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IEludGVsKFIpIDgyNTY3Vi0yIEdpZ2FiaXQgTmV0d29yayBDb25uZWN0aW9uCiAgIFBoeXNpY2FsIEFkZHJlc3MuIC4gLiAuIC4gLiAuIC4gLiA6IEY4LTBGLTQxLTE2LTg4LUU4CiAgIERIQ1AgRW5hYmxlZC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IE5vCiAgIEF1dG9jb25maWd1cmF0aW9uIEVuYWJsZWQgLiAuIC4gLiA6IFllcwogICBMaW5rLWxvY2FsIElQdjYgQWRkcmVzcyAuIC4gLiAuIC4gOiBmZTgwOjphOTkwOjM1ZTM6YTZhYjpmYzE1JTEwKFByZWZlcnJlZCkgCiAgIElQdjQgQWRkcmVzcy4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IDE3My4xODUuMTUzLjkzKFByZWZlcnJlZCkgCiAgIFN1Ym5ldCBNYXNrIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IDI1NS4yNTUuMjU1LjI0OAogICBEZWZhdWx0IEdhdGV3YXkgLiAuIC4gLiAuIC4gLiAuIC4gOiAxNzMuMTg1LjE1My44OQogICBESENQdjYgSUFJRCAuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiAyNTExMzc4NTcKICAgREhDUHY2IENsaWVudCBEVUlELiAuIC4gLiAuIC4gLiAuIDogMDAtMDEtMDAtMDEtMTYtM0ItM0YtQzItRjgtMEYtNDEtMTYtODgtRTgKICAgRE5TIFNlcnZlcnMgLiAuIC4gLiAuIC4gLiAuIC4gLiAuIDogMjA3LjkxLjUuMzIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMjA4LjY3LjIyMi4yMjIKICAgTmV0QklPUyBvdmVyIFRjcGlwLiAuIC4gLiAuIC4gLiAuIDogRW5hYmxlZAoKRXRoZXJuZXQgYWRhcHRlciBMb2NhbCBBcmVhIENvbm5lY3Rpb24qIDk6CgogICBNZWRpYSBTdGF0ZSAuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiBNZWRpYSBkaXNjb25uZWN0ZWQKICAgQ29ubmVjdGlvbi1zcGVjaWZpYyBETlMgU3VmZml4ICAuIDogCiAgIERlc2NyaXB0aW9uIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IEp1bmlwZXIgTmV0d29yayBDb25uZWN0IFZpcnR1YWwgQWRhcHRlcgogICBQaHlzaWNhbCBBZGRyZXNzLiAuIC4gLiAuIC4gLiAuIC4gOiAwMC1GRi1BMC04My00OC0wNAogICBESENQIEVuYWJsZWQuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiBZZXMKICAgQXV0b2NvbmZpZ3VyYXRpb24gRW5hYmxlZCAuIC4gLiAuIDogWWVzCgpUdW5uZWwgYWRhcHRlciBpc2F0YXAue0FBNDI2QjM3LTM2OTUtNEVCOC05OTBGLTRDRkFDODQ1RkQxN306CgogICBNZWRpYSBTdGF0ZSAuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiBNZWRpYSBkaXNjb25uZWN0ZWQKICAgQ29ubmVjdGlvbi1zcGVjaWZpYyBETlMgU3VmZml4ICAuIDogCiAgIERlc2NyaXB0aW9uIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IE1pY3Jvc29mdCBJU0FUQVAgQWRhcHRlcgogICBQaHlzaWNhbCBBZGRyZXNzLiAuIC4gLiAuIC4gLiAuIC4gOiAwMC0wMC0wMC0wMC0wMC0wMC0wMC1FMAogICBESENQIEVuYWJsZWQuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiBObwogICBBdXRvY29uZmlndXJhdGlvbiBFbmFibGVkIC4gLiAuIC4gOiBZZXMKClR1bm5lbCBhZGFwdGVyIFRlcmVkbyBUdW5uZWxpbmcgUHNldWRvLUludGVyZmFjZToKCiAgIENvbm5lY3Rpb24tc3BlY2lmaWMgRE5TIFN1ZmZpeCAgLiA6IAogICBEZXNjcmlwdGlvbiAuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiBUZXJlZG8gVHVubmVsaW5nIFBzZXVkby1JbnRlcmZhY2UKICAgUGh5c2ljYWwgQWRkcmVzcy4gLiAuIC4gLiAuIC4gLiAuIDogMDAtMDAtMDAtMDAtMDAtMDAtMDAtRTAKICAgREhDUCBFbmFibGVkLiAuIC4gLiAuIC4gLiAuIC4gLiAuIDogTm8KICAgQXV0b2NvbmZpZ3VyYXRpb24gRW5hYmxlZCAuIC4gLiAuIDogWWVzCiAgIElQdjYgQWRkcmVzcy4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IDIwMDE6MDo5ZDM4Ojk1M2M6MmNlZjo3ZmM6NTI0Njo2NmEyKFByZWZlcnJlZCkgCiAgIExpbmstbG9jYWwgSVB2NiBBZGRyZXNzIC4gLiAuIC4gLiA6IGZlODA6OjJjZWY6N2ZjOjUyNDY6NjZhMiUxMyhQcmVmZXJyZWQpIAogICBEZWZhdWx0IEdhdGV3YXkgLiAuIC4gLiAuIC4gLiAuIC4gOiAKICAgTmV0QklPUyBvdmVyIFRjcGlwLiAuIC4gLiAuIC4gLiAuIDogRGlzYWJsZWQKClR1bm5lbCBhZGFwdGVyIDZUTzQgQWRhcHRlcjoKCiAgIENvbm5lY3Rpb24tc3BlY2lmaWMgRE5TIFN1ZmZpeCAgLiA6IAogICBEZXNjcmlwdGlvbiAuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiBNaWNyb3NvZnQgNnRvNCBBZGFwdGVyICMyCiAgIFBoeXNpY2FsIEFkZHJlc3MuIC4gLiAuIC4gLiAuIC4gLiA6IDAwLTAwLTAwLTAwLTAwLTAwLTAwLUUwCiAgIERIQ1AgRW5hYmxlZC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IE5vCiAgIEF1dG9jb25maWd1cmF0aW9uIEVuYWJsZWQgLiAuIC4gLiA6IFllcwogICBJUHY2IEFkZHJlc3MuIC4gLiAuIC4gLiAuIC4gLiAuIC4gOiAyMDAyOmFkYjk6OTk1ZDo6YWRiOTo5OTVkKFByZWZlcnJlZCkgCiAgIERlZmF1bHQgR2F0ZXdheSAuIC4gLiAuIC4gLiAuIC4gLiA6IDIwMDI6YzA1ODo2MzAxOjpjMDU4OjYzMDEKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMjAwMjpjMDU4OjYzMDE6OjEKICAgRE5TIFNlcnZlcnMgLiAuIC4gLiAuIC4gLiAuIC4gLiAuIDogMjA3LjkxLjUuMzIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMjA4LjY3LjIyMi4yMjIKICAgTmV0QklPUyBvdmVyIFRjcGlwLiAuIC4gLiAuIC4gLiAuIDogRGlzYWJsZWQKClR1bm5lbCBhZGFwdGVyIGlzYXRhcC57QkExNjBGQzUtNzAyOC00QjFGLUEwNEItMUFDODAyQjBGRjVBfToKCiAgIE1lZGlhIFN0YXRlIC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IE1lZGlhIGRpc2Nvbm5lY3RlZAogICBDb25uZWN0aW9uLXNwZWNpZmljIEROUyBTdWZmaXggIC4gOiAKICAgRGVzY3JpcHRpb24gLiAuIC4gLiAuIC4gLiAuIC4gLiAuIDogTWljcm9zb2Z0IElTQVRBUCBBZGFwdGVyICMyCiAgIFBoeXNpY2FsIEFkZHJlc3MuIC4gLiAuIC4gLiAuIC4gLiA6IDAwLTAwLTAwLTAwLTAwLTAwLTAwLUUwCiAgIERIQ1AgRW5hYmxlZC4gLiAuIC4gLiAuIC4gLiAuIC4gLiA6IE5vCiAgIEF1dG9jb25maWd1cmF0aW9uIEVuYWJsZWQgLiAuIC4gLiA6IFllcwo=</rsp:Stream>
			<rsp:Stream CommandId="11111111-1111-1111-1111-111111111114" End="true" Name="stdout"/>
			<rsp:Stream CommandId="11111111-1111-1111-1111-111111111114" End="true" Name="stderr"/>
			<rsp:CommandState CommandId="11111111-1111-1111-1111-111111111114" State="http://schemas.microsoft.com/wbem/wsman/1/windows/shell/CommandState/Done">
				<rsp:ExitCode>0</rsp:ExitCode>
			</rsp:CommandState>
		</rsp:ReceiveResponse>
	</s:Body>
</s:Envelope>"""

def xml_str_compare(first, second):
    first_normalized = ET.tostring(ET.fromstring(first))
    second_normalized = ET.tostring(ET.fromstring(second))
    return first_normalized == second_normalized

class TransportStub(object):
    def send_message(self, message):
        if xml_str_compare(message, open_shell_request):
            return open_shell_response
        elif xml_str_compare(message, close_shell_request):
            return close_shell_response
        elif xml_str_compare(message, run_cmd_with_args_request) or xml_str_compare(message, run_cmd_wo_args_request):
            return run_cmd_response
        elif xml_str_compare(message, cleanup_cmd_request):
            return cleanup_cmd_response
        elif xml_str_compare(message, get_cmd_output_request):
            return get_cmd_output_response
        else:
            return None

class TestWinRMPrimitives(object):
    @classmethod
    def setup_class(cls):
        cls.uuid4_patcher = patch('uuid.uuid4')
        uuid4_mock = cls.uuid4_patcher.start()
        uuid4_mock.return_value = uuid.UUID('11111111-1111-1111-1111-111111111111')

        from winrm_service import WinRMWebService
        cls.winrm = WinRMWebService(
            endpoint='http://windows-host:5985/wsman',
            transport='plaintext',
            username='john.smith',
            password='secret')

        cls.winrm.transport = TransportStub()

    @classmethod
    def teardown_class(cls):
        cls.uuid4_patcher.stop()

    def test_open_shell_and_close_shell(self):
        shell_id = self.winrm.open_shell()
        assert shell_id == '11111111-1111-1111-1111-111111111113'

        self.winrm.close_shell(shell_id)

    def test_run_command_with_arguments_and_cleanup_command(self):
        shell_id = self.winrm.open_shell()
        command_id = self.winrm.run_command(shell_id, 'ipconfig', ['/all'])
        assert command_id == '11111111-1111-1111-1111-111111111114'

        self.winrm.cleanup_command(shell_id, command_id)
        self.winrm.close_shell(shell_id)

    def test_run_command_without_arguments_and_cleanup_command(self):
        shell_id = self.winrm.open_shell()
        command_id = self.winrm.run_command(shell_id, 'hostname')
        assert command_id == '11111111-1111-1111-1111-111111111114'

        self.winrm.cleanup_command(shell_id, command_id)
        self.winrm.close_shell(shell_id)

    def test_get_command_output(self):
        shell_id = self.winrm.open_shell()
        command_id = self.winrm.run_command(shell_id, 'ipconfig', ['/all'])
        stdout, stderr, return_code = self.winrm.get_command_output(shell_id, command_id)
        assert return_code == 0
        assert 'Windows IP Configuration' in stdout
        assert len(stderr) == 0

        self.winrm.cleanup_command(shell_id, command_id)
        self.winrm.close_shell(shell_id)