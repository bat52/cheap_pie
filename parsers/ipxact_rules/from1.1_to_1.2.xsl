<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- 
// 
// Revision:    $Revision: 1506 $
// Date:        $Date: 2009-04-25 23:51:56 -0700 (Sat, 25 Apr 2009) $
// 
// Copyright (c) 2005, 2006, 2007, 2009 The SPIRIT Consortium.
// 
// This work forms part of a deliverable of The SPIRIT Consortium.
// 
// Use of these materials are governed by the legal terms and conditions
// outlined in the disclaimer available from www.spiritconsortium.org.
// 
// This source file is provided on an AS IS basis.  The SPIRIT
// Consortium disclaims any warranty express or implied including
// any warranty of merchantability and fitness for use for a
// particular purpose.
// 
// The user of the source file shall indemnify and hold The SPIRIT
// Consortium and its members harmless from any damages or liability.
// Users are requested to provide feedback to The SPIRIT Consortium
// using either mailto:feedback@lists.spiritconsortium.org or the forms at 
// http://www.spiritconsortium.org/about/contact_us/
// 
// This file may be copied, and distributed, with or without
// modifications; this notice must be included on any copy.
  -->
<!--
// Description : from1.1_to1.2.xsl
// XSL transform to go from V1.1 version to V1.2 version of the Schema
// Author : SPIRIT Schema Working Group - Christophe Amerijckx
// Date:     February 2006
-->

<xsl:stylesheet version="2.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:spirit="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.1" xmlns:kactus2="http://funbase.cs.tut.fi/">

<xsl:output method="xml" indent="yes"/>

<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*"/>
            	<xsl:apply-templates/>
	</xsl:copy>
</xsl:template>

<!-- Changing element spirit:resetValue to spirit:reset with a subelement spirit:value -->

<xsl:template match="*/spirit:register/spirit:resetValue">
	<xsl:element name="spirit:reset">
		<xsl:element name="spirit:value"><xsl:value-of select="."/></xsl:element>
	</xsl:element>
</xsl:template>

<!-- Changing element spirit:hwModel to spirit:model -->

<xsl:template match="spirit:hwModel">
	<xsl:element name="spirit:model">
		<xsl:apply-templates select="@*"/>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>

<!-- Changing element spirit:hwParameters to spirit:modelParameters -->

<xsl:template match="*/spirit:hwParameters">
	<xsl:element name="spirit:modelParameters">
		<xsl:apply-templates select="@*"/>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>

<!-- Changing element spirit:hwParameter to spirit:modelParameter -->

<xsl:template match="*/spirit:hwParameter">
	<xsl:element name="spirit:modelParameter">
		<xsl:apply-templates select="@*"/>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>

<!-- Splitting interconnection attributes into activeInterfaces -->

<xsl:template match="*/spirit:interconnection">
	<xsl:element name="spirit:interconnection">
		<xsl:element name="spirit:activeInterface">
			<xsl:attribute name="spirit:componentRef"><xsl:value-of select="@spirit:component1Ref"/></xsl:attribute>
			<xsl:attribute name="spirit:busRef"><xsl:value-of select="@spirit:busInterface1Ref"/></xsl:attribute>
		</xsl:element>
		<xsl:element name="spirit:activeInterface">
			<xsl:attribute name="spirit:componentRef"><xsl:value-of select="@spirit:component2Ref"/></xsl:attribute>
			<xsl:attribute name="spirit:busRef"><xsl:value-of select="@spirit:busInterface2Ref"/></xsl:attribute>
		</xsl:element>
	</xsl:element>
</xsl:template>

<!-- Add :: to envIdentifier -->

<xsl:template match="spirit:component/spirit:hwModel/spirit:views/spirit:view/spirit:envIdentifier">
    <xsl:element name="spirit:envIdentifier">:<xsl:value-of select="."/>:</xsl:element>
</xsl:template>

<!-- Removing spirit:component/spirit:interconnections -->

<xsl:template match="spirit:component/spirit:interconnections">
</xsl:template>

<!-- Removing spirit:component/spirit:componentInstances -->

<xsl:template match="spirit:component/spirit:componentInstances">
</xsl:template>

<!-- Removing spirit:component/spirit:busInterfaces/spirit:businterface/spirit:exportedInterface -->

<xsl:template match="spirit:component/spirit:busInterfaces/spirit:businterface/spirit:exportedInterface">
</xsl:template>

<!-- Changing spirit:swFunction to spirit:function -->

<xsl:template match="*/spirit:swFunction">
	<xsl:element name="spirit:function">
		<xsl:apply-templates select="@*"/>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>

<!-- putting spirit: before log, decode, pow and containsToken in dependencies -->

<xsl:template match="@spirit:dependency">
	<xsl:attribute name="spirit:dependency">
		<xsl:value-of select="replace(replace(replace(replace(.,'pow','spirit:pow'),'containsToken','spirit:containsToken'),'decode','spirit:decode'),'log','spirit:log')"/>
	</xsl:attribute>
</xsl:template>

<!-- remove default signal strength in a bus definition -->

<xsl:template match="spirit:busDefinition/spirit:signals/spirit:signal/spirit:defaultValue/spirit:strength">
</xsl:template>

<!-- Adding name to channel with generated ID -->

<xsl:template match="spirit:channel">
	<xsl:element name="spirit:channel">
		<xsl:apply-templates select="@*"/>
		<xsl:element name="spirit:name">
			<xsl:text>InternalID</xsl:text><xsl:value-of select="generate-id(.)"/>
		</xsl:element>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>

<!-- Adding version to design if not existing -->

<xsl:template match="spirit:design">
	<xsl:copy>
		<xsl:apply-templates select="@*"/>
		<xsl:choose>
			<xsl:when test="not(spirit:version)">
				<xsl:apply-templates select="spirit:vendor|spirit:library|spirit:name"/>
				<xsl:element name="spirit:version">
					<xsl:text>unset</xsl:text>
				</xsl:element>
				<xsl:apply-templates select="spirit:componentInstances|spirit:interconnections|spirit:adHocConnections|spirit:vendorExtensions"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>