<!-- 
// Copyright (c) 2005 - 2012 Accellera Systems Initiative Inc. 
// All rights reserved.
//
// THIS WORK FORMS PART OF A ACCELLERA SYSTEMS INITIATIVE SPECIFICATION.
// USE OF THESE MATERIALS ARE GOVERNED BY
// THE LEGAL TERMS AND CONDITIONS OUTLINED IN THE IPXACT
// SPECIFICATION DISCLAIMER AVAILABLE FROM
// www.accellera.org
//
// This source file is provided on an AS IS basis. The Accellera Systems Initiative disclaims 
// ANY WARRANTY EXPRESS OR IMPLIED INCLUDING ANY WARRANTY OF
// MERCHANTABILITY AND FITNESS FOR USE FOR A PARTICULAR PURPOSE. 
// The user of the source file shall indemnify and hold The Accellera Systems Initiative
// harmless from any damages or liability arising out of the use thereof or the 
// performance or implementation or partial implementation of the schema.
  -->
<!--
// Description :  from1685_2009_to_1685_2014.xsl
// XSL transform to go from the 1685-2009 version to the 1685-2014 version of the Schema
// Author: The Accellera System Initiative IP-XACT Schema Working Group
// Date: July 5, 2012
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:spirit="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009" xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2014" version="1.0" xmlns:xalan="http://xml.apache.org/xalan" xmlns:exslt="http://exslt.org/common" xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="xalan exslt msxsl spirit" xmlns:kactus2="http://funbase.cs.tut.fi/">
	<xsl:import href="convert_expressions-other.xsl"/>
	<xsl:import href="convert_expressions-exslt.xsl"/>
	<xsl:import href="convert_expressions-msxsl.xsl"/>
	<xsl:import href="convert_expressions-xalan.xsl"/>
	
	<xsl:param name="catalog"/>
	<xsl:param name="createDesignInstantiation" select="true()"/>
	<xsl:param name="verbose" select="true()"/>
	<xsl:param name="namespace" select="'http://www.accellera.org/XMLSchema/IPXACT/1685-2014'"/>
	<xsl:param name="prefix" select="true()"/>
	<xsl:strip-space elements="*"/>
	<xsl:output method="xml" indent="yes"/>
	
	<xsl:template match="kactus2:systemView/ipxact:hierarchyRef">
			<kactus2:hierarchyRef><xsl:apply-templates select="@*|node()" /></kactus2:hierarchyRef>
    </xsl:template>
	
	<xsl:template match="kactus2:swView/ipxact:hierarchyRef">
			<kactus2:hierarchyRef><xsl:apply-templates select="@*|node()" /></kactus2:hierarchyRef>
    </xsl:template>
	
	<xsl:template match="kactus2:swInstance/ipxact:instanceName">
			<kactus2:instanceName><xsl:apply-templates select="@*|node()" /></kactus2:instanceName>
    </xsl:template>
	
	<xsl:template match="kactus2:swInstance/ipxact:displayName">
			<kactus2:displayName><xsl:apply-templates select="@*|node()" /></kactus2:displayName>
    </xsl:template>
 
	<xsl:template match="kactus2:swInstance/ipxact:description">
			<kactus2:description><xsl:apply-templates select="@*|node()" /></kactus2:description>
    </xsl:template>
	
	<xsl:param name="pReplacement" select="'Flat'"/>

	<xsl:template match="kactus2:kts_productHier/text()[.='Global']">
		<xsl:value-of select="$pReplacement"/>
	</xsl:template>
	
	<xsl:template match="@kactus2:*">
	   <xsl:attribute name="{local-name()}">
		  <xsl:value-of select="."/>
	   </xsl:attribute>
	</xsl:template>
	
	<xsl:template match="ipxact:vendorExtensions">
		<xsl:for-each select="kactus2:array">
			<ipxact:arrays>
				<ipxact:array>
					<ipxact:left><xsl:apply-templates select='kactus2:left/node()'/></ipxact:left>
					<ipxact:right><xsl:apply-templates select='kactus2:right/node()'/></ipxact:right>
				</ipxact:array>
			</ipxact:arrays>
		</xsl:for-each>
		<xsl:copy>
            <xsl:apply-templates select="node()[not(name() = 'kactus2:array') and not(name() = 'kactus2:extensions')] | kactus2:extensions/node()"/>
		</xsl:copy>
    </xsl:template>
	
    <xsl:template match="kactus2:apiDependencies/kactus2:apiDependency">
        <kactus2:apiConnection><xsl:apply-templates select="@*|node()" /></kactus2:apiConnection>
    </xsl:template>
	
    <xsl:template match="kactus2:apiDependencies">
        <kactus2:apiConnections><xsl:apply-templates select="@*|node()" /></kactus2:apiConnections>
    </xsl:template>

	<!-- Process the document node. -->
	<xsl:template match="/">
		<xsl:apply-templates select="comment() | processing-instruction()"/>
		<xsl:apply-templates select="*"/>
	</xsl:template>
	<xsl:template match="*">
		<xsl:element name="{name()}" namespace="{namespace-uri()}">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>
	<!-- Copy comments, pi's and text. -->
	<xsl:template match="comment() | processing-instruction()">
		<xsl:copy>
			<xsl:apply-templates/>
		</xsl:copy>
		<xsl:text>
</xsl:text>
	</xsl:template>
	<xsl:template name="insertComment">
		<xsl:param name="number"/>
		<xsl:param name="message"/>
		<xsl:if test="$verbose">
			<xsl:message>IP-XACT 1685-2014 XSLT Warning#<xsl:value-of select="$number"/>: <xsl:value-of select="$message"/>
			</xsl:message>
		</xsl:if>
		<xsl:comment> IP-XACT 1685-2014 XSLT Warning#<xsl:value-of select="$number"/>: <xsl:value-of select="$message"/>
		</xsl:comment>
	</xsl:template>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}" namespace="{namespace-uri()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="/spirit:*">
		<xsl:element name="ipxact:{local-name()}" namespace="{$namespace}">
			<xsl:for-each select="namespace::*">
				<xsl:if test="not(.='http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009')">
					<xsl:copy/>
				</xsl:if>
			</xsl:for-each>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@xsi:schemaLocation">
		<xsl:attribute name="xsi:schemaLocation"><xsl:text>http://www.accellera.org/XMLSchema/IPXACT/1685-2014 http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd</xsl:text></xsl:attribute>
	</xsl:template>
	<xsl:template match="spirit:*">
		<xsl:element name="ipxact:{local-name()}" namespace="{$namespace}">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>
	
</xsl:stylesheet>
