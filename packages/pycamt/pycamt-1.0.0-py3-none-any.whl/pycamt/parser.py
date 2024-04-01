from io import StringIO

from defusedxml import ElementTree as ET


class Camt053Parser:
    """
    A parser class for camt.053 XML files, designed to be flexible and extensible for different CAMT.053 versions.

    Attributes
    ----------
    tree : ElementTree
        An ElementTree object representing the parsed XML document.
    namespaces : dict
        A dictionary of XML namespaces extracted from the document for XPath queries.
    version : str
        The CAMT.053 version detected in the XML document.

    Methods
    -------
    from_file(cls, file_path):
        Creates an instance of Camt053Parser from a file.

    get_group_header():
        Extracts group header information from the CAMT.053 file.

    get_transactions():
        Extracts all transaction entries from the CAMT.053 file.

    get_statement_info():
        Extracts statement information like IBAN and balances from the CAMT.053 file.
    """

    def __init__(self, xml_data):
        """
        Initializes the Camt053Parser with XML data.

        Parameters
        ----------
        xml_data : str
            XML data as a string representation of CAMT.053 content.
        """
        self.tree = ET.fromstring(xml_data)
        self.namespaces = self._detect_namespaces(xml_data)
        self.version = self._detect_version()

    @classmethod
    def from_file(cls, file_path):
        """
        Creates an instance of Camt053Parser from a CAMT.053 XML file.

        Parameters
        ----------
        file_path : str
            The file path to the CAMT.053 XML file.

        Returns
        -------
        Camt053Parser
            An instance of the parser initialized with the XML content from the file.
        """
        with open(file_path, encoding="utf-8") as file:
            xml_data = file.read()
        return cls(xml_data)

    def _detect_namespaces(self, xml_data):
        """
        Detects and extracts namespaces from the XML data for XPath queries.

        Parameters
        ----------
        xml_data : str
            XML data from which namespaces are to be extracted.

        Returns
        -------
        dict
            A dictionary of namespace prefixes to namespace URIs.
        """
        namespaces = {}
        for _, elem in ET.iterparse(StringIO(xml_data), events=("start-ns",)):
            namespaces[elem[0]] = elem[1]
        return namespaces

    def _detect_version(self):
        """
        Detects the CAMT.053 version from the XML root element.

        Returns
        -------
        str
            The detected CAMT.053 version or 'unknown' if the version cannot be determined.
        """
        root = self.tree
        for version in [
            "camt.053.001.02",
            "camt.053.001.03",
            "camt.053.001.04",
        ]:
            if version in root.tag:
                return version
        return "unknown"

    def get_group_header(self):
        """
        Extracts the group header information from the CAMT.053 file.

        Returns
        -------
        dict
            A dictionary containing the extracted group header information, such as message ID and creation date/time.
        """
        grp_hdr = self.tree.find(".//GrpHdr", self.namespaces)
        if grp_hdr is not None:
            return self._extract_group_header(grp_hdr)
        return {}

    def _extract_group_header(self, grp_hdr):
        """
        Extracts information from the group header element.

        Parameters
        ----------
        grp_hdr : Element
            The XML element representing the group header.

        Returns
        -------
        dict
            Extracted information including message ID and creation date/time.
        """
        msg_id = grp_hdr.find(".//MsgId", self.namespaces).text
        cre_dt_tm = grp_hdr.find(".//CreDtTm", self.namespaces).text
        return {"MessageID": msg_id, "CreationDateTime": cre_dt_tm}

    def get_transactions(self):
        """
        Extracts all transactions from the CAMT.053 file.

        Returns
        -------
        list of dict
            A list of dictionaries, each representing a transaction with its associated data.
        """
        transactions = []
        entries = self.tree.findall(".//Ntry", self.namespaces)
        for entry in entries:
            transactions.extend(self._extract_transaction(entry))
        return transactions

    def _extract_transaction(self, entry):
        """
        Extracts data from a single transaction entry.

        Parameters
        ----------
        entry : Element
            The XML element representing a transaction entry.

        Returns
        -------
        dict
            A dictionary containing extracted data for the transaction.
        """

        common_data = self._extract_common_entry_data(entry)
        entry_details = entry.findall(".//NtryDtls", self.namespaces)

        transactions = []

        # Handle 1-0 relationship
        if not entry_details:
            transactions.append(common_data)
        else:
            for ntry_detail in entry_details:
                tx_details = ntry_detail.findall(".//TxDtls", self.namespaces)

                # Handle 1-1 relationship
                if len(tx_details) == 1:
                    transactions.append(
                        {
                            **common_data,
                            **self._extract_transaction_details(tx_details[0]),
                        }
                    )

                # Handle 1-n relationship
                else:
                    for tx_detail in tx_details:
                        transactions.append(
                            {
                                **common_data,
                                **self._extract_transaction_details(tx_detail),
                            }
                        )
        return transactions

    def _extract_common_entry_data(self, entry):
        """
        Extracts common data applicable to all transactions within an entry.

        Parameters
        ----------
        entry : Element
            The XML element representing an entry.

        Returns
        -------
        dict
            A dictionary containing common data extracted from the entry.
        """
        return {
            "Amount": entry.find(".//Amt", self.namespaces).text,
            "Currency": entry.find(".//Amt", self.namespaces).attrib.get("Ccy"),
            "CreditDebitIndicator": entry.find(".//CdtDbtInd", self.namespaces).text,
            "ReversalIndicator": (
                entry.find(".//RvslInd", self.namespaces).text
                if entry.find(".//RvslInd", self.namespaces) is not None
                else None
            ),
            "Status": (
                entry.find(".//Sts", self.namespaces).text
                if entry.find(".//Sts", self.namespaces) is not None
                else None
            ),
            "BookingDate": entry.find(".//BookgDt//Dt", self.namespaces).text,
            "ValueDate": entry.find(".//ValDt//Dt", self.namespaces).text,
            "BankTransactionCode": (
                entry.find(".//BkTxCd//Domn//Cd", self.namespaces).text
                if entry.find(".//BkTxCd//Domn//Cd", self.namespaces) is not None
                else None
            ),
            "TransactionFamilyCode": (
                entry.find(".//BkTxCd//Domn//Fmly//Cd", self.namespaces).text
                if entry.find(".//BkTxCd//Domn//Fmly//Cd", self.namespaces) is not None
                else None
            ),
            "TransactionSubFamilyCode": (
                entry.find(".//BkTxCd//Domn//Fmly//SubFmlyCd", self.namespaces).text
                if entry.find(".//BkTxCd//Domn//Fmly//SubFmlyCd", self.namespaces) is not None
                else None
            ),
            "AdditionalEntryInformation": (
                entry.find(".//AddtlNtryInf", self.namespaces).text
                if entry.find(".//AddtlNtryInf", self.namespaces) is not None
                else None
            ),
        }

    def _extract_transaction_details(self, tx_detail):
        """
        Extracts details specific to a transaction.

        Parameters
        ----------
        tx_detail : Element
            The XML element representing transaction details.

        Returns
        -------
        dict
            Detailed information extracted from the transaction detail element.
        """

        return {
            "EndToEndId": (
                tx_detail.find(".//Refs//EndToEndId", self.namespaces).text
                if tx_detail.find(".//Refs//EndToEndId", self.namespaces) is not None
                else None
            ),
            "MandateId": (
                tx_detail.find(".//Refs//MndtId", self.namespaces).text
                if tx_detail.find(".//Refs//MndtId", self.namespaces) is not None
                else None
            ),
            "Amount": (
                tx_detail.find(".//Amt", self.namespaces).text
                if tx_detail.find(".//Amt", self.namespaces) is not None
                else None
            ),
            "CreditorName": (
                tx_detail.find(".//RltdPties//Cdtr//Nm", self.namespaces).text
                if tx_detail.find(".//RltdPties//Cdtr//Nm", self.namespaces) is not None
                else None
            ),
            "DebtorName": (
                tx_detail.find(".//RltdPties//Dbtr//Nm", self.namespaces).text
                if tx_detail.find(".//RltdPties//Dbtr//Nm", self.namespaces) is not None
                else None
            ),
            "RemittanceInformation": (
                tx_detail.find(".//RmtInf//Ustrd", self.namespaces).text
                if tx_detail.find(".//RmtInf//Ustrd", self.namespaces) is not None
                else None
            ),
        }

    def get_statement_info(self):
        """
        Extracts basic statement information like IBAN, opening, and closing balance.

        Returns
        -------
        dict
            A dictionary containing statement information.
        """
        stmt = self.tree.find(".//Stmt", self.namespaces)
        if stmt is not None:
            iban = stmt.find(".//Acct//Id//IBAN", self.namespaces)
            iban_text = iban.text if iban is not None else None
            op_bal = stmt.find(".//Bal//Amt", self.namespaces)
            op_bal_text = op_bal.text if op_bal is not None else None
            return {"IBAN": iban_text, "OpeningBalance": op_bal_text}
        return {}
