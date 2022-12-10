<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xalan="http://xml.apache.org/xalan" xmlns:exslt="http://exslt.org/common" exclude-result-prefixes="xalan exslt msxsl temp" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:temp="http://www.accellera.org/temp" xmlns:kactus2="http://funbase.cs.tut.fi/">
	<xsl:output method="xml" indent="yes" encoding="UTF-8"/>

	<xsl:param name="debug" select="false()"/>
	<xsl:variable name="apos">&apos;</xsl:variable>
	<xsl:variable name="quot">&quot;</xsl:variable>

	<xsl:template name="parse-scale">
		<xsl:param name="value" select="."/>
		<xsl:param name="bit-length" select="0"/>
                <xsl:if test="$debug">
	                <xsl:message>parse-scale(<xsl:value-of select="$value"/>, <xsl:value-of select="$bit-length"/>)</xsl:message>
                </xsl:if>
		<xsl:choose>
			<xsl:when test="starts-with($value, '&quot;')">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
				</xsl:if>
				<xsl:text>'b</xsl:text>
				<xsl:value-of select="substring-before(substring-after($value,'&quot;'),'&quot;')"/>
			</xsl:when>
			<xsl:when test="starts-with($value, '0x')">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
				</xsl:if>
				<xsl:text>'h</xsl:text>
				<xsl:call-template name="parse-scale">
					<xsl:with-param name="value" select="substring-after($value,'0x')"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="starts-with($value, '0X')">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
				</xsl:if>
				<xsl:text>'h</xsl:text>
				<xsl:call-template name="parse-scale">
					<xsl:with-param name="value" select="substring-after($value,'0X')"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="starts-with($value, '#')">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
				</xsl:if>
				<xsl:text>'h</xsl:text>
				<xsl:call-template name="parse-scale">
					<xsl:with-param name="value" select="substring-after($value,'#')"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="contains($value, 'k') and number(substring-before($value, 'k'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 'k')"/>
				<xsl:text> * (2 ** 10)</xsl:text>
			</xsl:when>
			<xsl:when test="contains($value, 'K') and number(substring-before($value, 'K'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 'K')"/>
				<xsl:text> * (2 ** 10)</xsl:text>
			</xsl:when>
			<xsl:when test="contains($value, 'm') and number(substring-before($value, 'm'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 'm')"/>
				<xsl:text> * (2 ** 20)</xsl:text>
			</xsl:when>
			<xsl:when test="contains($value, 'M') and number(substring-before($value, 'M'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 'M')"/>
				<xsl:text> * (2 ** 20)</xsl:text>
			</xsl:when>
			<xsl:when test="contains($value, 'g') and number(substring-before($value, 'g'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 'g')"/>
				<xsl:text> * (2 ** 30)</xsl:text>
			</xsl:when>
			<xsl:when test="contains($value, 'G') and number(substring-before($value, 'G'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 'G')"/>
				<xsl:text> * (2 ** 30)</xsl:text>
			</xsl:when>
			<xsl:when test="contains($value, 't') and number(substring-before($value, 't'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 't')"/>
				<xsl:text> * (2 ** 40)</xsl:text>
			</xsl:when>
			<xsl:when test="contains($value, 'T') and number(substring-before($value, 'T'))">
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="substring-before($value, 'T')"/>
				<xsl:text> * (2 ** 40)</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="$debug">
					<xsl:message>otherwise: <xsl:value-of select="$value"/></xsl:message>
				</xsl:if>
				<xsl:if test="$bit-length > 0">
					<xsl:value-of select="$bit-length"/>
					<xsl:text>'d</xsl:text>
				</xsl:if>
				<xsl:value-of select="$value"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="tokenize">
		<xsl:param name="value" select="''"/>
		<xsl:param name="delimiters" select="' &#x9;&#xA;'"/>
		<xsl:if test="$debug">
			<xsl:message>tokenize("<xsl:value-of select="$value"/>", "<xsl:value-of select="$delimiters"/>")</xsl:message>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="not($value)"/>
			<xsl:when test="not($delimiters)">
				<xsl:call-template name="_tokenize-characters">
					<xsl:with-param name="value" select="$value"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="_tokenize-delimiters">
					<xsl:with-param name="value" select="$value"/>
					<xsl:with-param name="delimiters" select="$delimiters"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="_tokenize-characters">
		<xsl:param name="value"/>
		<xsl:if test="$value">
			<token>
				<xsl:value-of select="substring($value, 1, 1)"/>
			</token>
			<xsl:call-template name="_tokenize-characters">
				<xsl:with-param name="value" select="substring($value, 2)"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>

	<xsl:template name="_tokenize-delimiters">
		<xsl:param name="value"/>
		<xsl:param name="delimiters"/>
		<xsl:variable name="delimiter" select="substring($delimiters, 1, 1)"/>
		<xsl:if test="$debug">
			<xsl:message>_tokenize-delimiters("<xsl:value-of select="$value"/>", "<xsl:value-of select="$delimiters"/>")</xsl:message>
		</xsl:if>
		<xsl:if test="string-length($value) > 0">
			<xsl:choose>
				<xsl:when test="not($delimiter)">
					<token>
						<xsl:value-of select="$value"/>
					</token>
				</xsl:when>
				<xsl:when test="contains($value, $delimiter)">
					<xsl:if test="not(starts-with($value, $delimiter))">
						<xsl:call-template name="_tokenize-delimiters">
							<xsl:with-param name="value" select="substring-before($value, $delimiter)"/>
							<xsl:with-param name="delimiters" select="substring($delimiters, 2)"/>
						</xsl:call-template>
					</xsl:if>
					<xsl:if test="$delimiter != '&#x20;'">
						<token type="delimiter">
							<xsl:value-of select="$delimiter"/>
						</token>
					</xsl:if>
					<xsl:choose>
						<xsl:when test="$delimiter = $apos or $delimiter = $quot">
							<xsl:call-template name="_tokenize-string">
								<xsl:with-param name="value" select="substring-after($value, $delimiter)"/>
								<xsl:with-param name="delimiter" select="$delimiter"/>
								<xsl:with-param name="delimiters" select="$delimiters"/>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="_tokenize-delimiters">
								<xsl:with-param name="value" select="substring-after($value, $delimiter)"/>
								<xsl:with-param name="delimiters" select="$delimiters"/>
							</xsl:call-template>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="_tokenize-delimiters">
						<xsl:with-param name="value" select="$value"/>
						<xsl:with-param name="delimiters" select="substring($delimiters, 2)"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>

	<xsl:template name="_tokenize-string">
		<xsl:param name="value"/>
		<xsl:param name="delimiter"/>
		<xsl:param name="delimiters"/>
		<xsl:if test="$debug">
			<xsl:message>_tokenize-string("<xsl:value-of select="$value"/>", "<xsl:value-of select="$delimiter"/>")</xsl:message>
		</xsl:if>
		<xsl:if test="string-length($value) > 0">
			<xsl:choose>
				<xsl:when test="contains($value, $delimiter)">
					<xsl:if test="not(starts-with($value, $delimiter))">
						<token type="string">
							<xsl:value-of select="substring-before($value, $delimiter)"/>
						</token>
					</xsl:if>
					<token type="delimiter">
						<xsl:value-of select="$delimiter"/>
					</token>
					<xsl:call-template name="_tokenize-delimiters">
						<xsl:with-param name="value" select="substring-after($value, $delimiter)"/>
						<xsl:with-param name="delimiters" select="$delimiters"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<token type="string">
						<xsl:value-of select="$value"/>
					</token>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>

	<xsl:template name="add-space">
		<xsl:param name="next-token" select="''"/>
		<xsl:if test="$next-token != '(' and $next-token != ')' and $next-token != ','">
			<xsl:text> </xsl:text>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
